from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List

from .base import Agent, TaskRequest, TaskResponse


class FileAgent(Agent):
    """Agent for simple file operations."""

    def handle(self, request: TaskRequest) -> TaskResponse:
        parts = request.content.split(maxsplit=1)

        if not parts:
            return TaskResponse(content="No command provided")
        command = parts[0]
        argument: Optional[str] = parts[1] if len(parts) > 1 else None

        if command == "read" and argument:
            return self._read_file(argument)
        if command == "write" and argument:
            name, _, body = argument.partition(" ")
            return self._write_file(name, body)
        if command == "list" and argument:
            return self._list_directory(argument)
        return TaskResponse(content="Unknown file command. Supported commands: read, write, list")

    def _read_file(self, file_path: str) -> TaskResponse:
        """Read a file with proper encoding handling."""
        path = Path(file_path)
        if not path.exists():
            return TaskResponse(content=f"File {file_path} not found")
            
        # Try different encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
        last_error = None
        
        for encoding in encodings:
            try:
                content = path.read_text(encoding=encoding)
                return TaskResponse(content=content)
            except UnicodeDecodeError as e:
                last_error = e
                continue
            except Exception as e:
                return TaskResponse(content=f"Error reading file: {str(e)}")
                
        return TaskResponse(content=f"Could not decode file with any of the attempted encodings. Last error: {str(last_error)}")

    def _write_file(self, file_path: str, content: str) -> TaskResponse:
        """Write content to a file."""
        try:
            path = Path(file_path)
            path.write_text(content, encoding='utf-8')
            return TaskResponse(content=f"Successfully wrote to {file_path}")
        except Exception as e:
            return TaskResponse(content=f"Error writing to file: {str(e)}")

    def _list_directory(self, dir_path: str) -> TaskResponse:
        """List contents of a directory."""
        try:
            path = Path(dir_path)
            if not path.exists():
                return TaskResponse(content=f"Directory {dir_path} not found")
            if not path.is_dir():
                return TaskResponse(content=f"{dir_path} is not a directory")
                
            items = []
            for item in path.iterdir():
                item_type = "dir" if item.is_dir() else "file"
                items.append(f"{item_type}: {item.name}")
                
            return TaskResponse(content="\n".join(items))
        except Exception as e:
            return TaskResponse(content=f"Error listing directory: {str(e)}")
