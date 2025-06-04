#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

import textnode as tnd
from blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    logging.info(
        f"Generating page from {from_path} to {dest_path} using template {template_path}"
    )
    if not from_path.exists():
        raise FileNotFoundError(f"Source file {from_path} does not exist.")
    if not template_path.exists():
        raise FileNotFoundError(f"Template file {template_path} does not exist.")

    markdown_file = from_path.read_text(encoding="utf-8")
    html_content = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)

    # Load templates from the current directory
    env = Environment(loader=FileSystemLoader("."))
    # Load your template.html
    template = env.get_template(template_path.name)

    # Render with your data
    html_file = template.render(Title=title, Content=html_content)

    # create destination directory if it does not exist
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(html_file, encoding="utf-8")


def extract_title(markdown):
    """
    Extract the # header line of the markdown as the title.
    """
    lines = markdown.splitlines()
    if not lines:
        return ""
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def delete_files_in_directory(directory):
    if not directory.exists():
        raise FileNotFoundError(f"Directory {directory} does not exist.")
    # Safety check to ensure directory name makes sense
    # Not / or "", ., ..
    if directory.name in ["/", ".", "..", ""]:
        raise ValueError("Invalid directory name for deletion.")

    logging.info(f"Deleting files in directory: {directory}")
    for item in directory.iterdir():
        if item.is_file():
            logging.info(f"Deleting file: {item}")
            item.unlink()
        elif item.is_dir():
            logging.info(f"Recursively deleting directory: {item}")
            delete_files_in_directory(item)
            item.rmdir()


def provision_static_assets(source, destination):
    logging.info(f"Provisioning static assets from {source} to {destination}")

    # Should we move this out?
    # Considering static and dynamic content - that can cause hard to catch bugs
    delete_files_in_directory(destination)

    logging.info(f"Copying files from {source} to {destination}")

    for item in source.iterdir():
        if item.is_file():
            logging.info(f"Copying file: {item} to {destination}")
            destination_file = destination / item.name
            destination_file.write_bytes(item.read_bytes())
        elif item.is_dir():
            logging.info(f"Recursively copying directory: {item} to {destination}")
            new_destination = destination / item.name
            new_destination.mkdir(parents=True, exist_ok=True)
            provision_static_assets(item, new_destination)


def gather_markdown_files(dir_path):
    """
    Gather all markdown files in the given directory and its subdirectories.
    """
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory {dir_path} does not exist.")

    markdown_files = []
    for item in dir_path.rglob("*.md"):
        if item.is_file():
            markdown_files.append(item)

    return markdown_files


def generate_pages_recursive(source, template_path, destination):
    if not source.exists():
        raise FileNotFoundError(f"Source directory {source} does not exist.")
    if not template_path.exists():
        raise FileNotFoundError(f"Template file {template_path} does not exist.")
    if not destination.exists():
        raise FileNotFoundError(f"Destination directory {destination} does not exist.")

    markdown_files = gather_markdown_files(source)

    for markdown_file in markdown_files:
        dest_path = destination / markdown_file.relative_to(source).with_suffix(".html")
        try:
            generate_page(
                from_path=markdown_file,
                template_path=template_path,
                dest_path=dest_path,
            )
            logging.info(f"Generated HTML page for {markdown_file}")
        except Exception as e:
            logging.error(f"Error generating page for {markdown_file}: {e}")
            raise


def main():
    # Configure root logger once, at program entry
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting static asset provisioning...")
    static_source = Path("static")
    destination = Path("public")

    try:
        provision_static_assets(static_source, destination)
        logging.info("Static assets provisioned successfully.")
    except Exception as e:
        logging.error(f"Error during static asset provisioning: {e}")
        raise

    logging.info("Generating HTML pages from markdown files...")

    content_source = Path("content")
    template_file = Path("template.html")

    generate_pages_recursive(
        source=content_source,
        template_path=template_file,
        destination=destination,
    )


if __name__ == "__main__":
    main()
