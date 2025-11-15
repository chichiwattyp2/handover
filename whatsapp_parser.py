"""
WhatsApp Chat Parser Module
Parses WhatsApp exported chat files and extracts structured data
"""

import re
from datetime import datetime
from typing import List, Dict, Optional
from dateutil import parser as date_parser


class WhatsAppMessage:
    """Represents a single WhatsApp message"""

    def __init__(self, timestamp: datetime, sender: str, content: str, is_system: bool = False):
        self.timestamp = timestamp
        self.sender = sender
        self.content = content
        self.is_system = is_system

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'sender': self.sender,
            'content': self.content,
            'is_system': self.is_system
        }


class WhatsAppChatParser:
    """Parses WhatsApp chat export files"""

    # Different WhatsApp export formats
    PATTERNS = [
        # Format: 1/15/25, 10:30 AM - John: Message
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}(?:\s*[AP]M)?)\s*[-–]\s*([^:]+?):\s*(.*)',
        # Format: [1/15/25, 10:30:45 AM] John: Message
        r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\]\s*([^:]+?):\s*(.*)',
        # Format: 15/01/25, 10:30 - John: Message (DD/MM/YY)
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}(?::\d{2})?)\s*[-–]\s*([^:]+?):\s*(.*)',
        # Format: 2025-01-15, 10:30 - John: Message (ISO-like)
        r'(\d{4}-\d{1,2}-\d{1,2},\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\s*[-–]\s*([^:]+?):\s*(.*)',
    ]

    # System message patterns (notifications, not actual messages)
    SYSTEM_PATTERNS = [
        r'Messages and calls are end-to-end encrypted',
        r'changed the subject',
        r'changed this group\'s icon',
        r'added',
        r'left',
        r'removed',
        r'You created group',
        r'created group',
        r'changed their phone number',
        r'security code changed',
    ]

    def __init__(self):
        self.messages: List[WhatsAppMessage] = []

    def parse(self, content: str) -> List[WhatsAppMessage]:
        """
        Parse WhatsApp chat content and return list of messages

        Args:
            content: Raw text content from WhatsApp export

        Returns:
            List of WhatsAppMessage objects
        """
        self.messages = []
        lines = content.split('\n')

        current_message = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try to match message patterns
            matched = False
            for pattern in self.PATTERNS:
                match = re.match(pattern, line)
                if match:
                    # If we have a previous message, save it
                    if current_message:
                        self.messages.append(current_message)

                    timestamp_str, sender, content = match.groups()

                    # Parse timestamp
                    try:
                        timestamp = self._parse_timestamp(timestamp_str)
                    except:
                        # If timestamp parsing fails, skip this line
                        continue

                    # Check if it's a system message
                    is_system = self._is_system_message(content)

                    current_message = WhatsAppMessage(
                        timestamp=timestamp,
                        sender=sender.strip(),
                        content=content.strip(),
                        is_system=is_system
                    )
                    matched = True
                    break

            # If line doesn't match a new message, it's a continuation of previous message
            if not matched and current_message:
                current_message.content += '\n' + line

        # Don't forget the last message
        if current_message:
            self.messages.append(current_message)

        return self.messages

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp string to datetime object"""
        # Clean up the timestamp string
        timestamp_str = timestamp_str.strip()

        # Try fuzzy parsing which handles various formats
        try:
            return date_parser.parse(timestamp_str, fuzzy=True)
        except:
            # Fallback: try common formats explicitly
            formats = [
                '%m/%d/%y, %I:%M %p',
                '%m/%d/%Y, %I:%M %p',
                '%d/%m/%y, %H:%M',
                '%d/%m/%Y, %H:%M',
                '%Y-%m-%d, %H:%M',
                '%m/%d/%y, %H:%M:%S',
                '%d/%m/%y, %H:%M:%S',
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(timestamp_str, fmt)
                except:
                    continue

            raise ValueError(f"Could not parse timestamp: {timestamp_str}")

    def _is_system_message(self, content: str) -> bool:
        """Check if message is a system notification"""
        for pattern in self.SYSTEM_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False

    def get_participants(self) -> List[str]:
        """Get list of unique participants (excluding system messages)"""
        participants = set()
        for msg in self.messages:
            if not msg.is_system:
                participants.add(msg.sender)
        return sorted(list(participants))

    def get_message_count(self) -> int:
        """Get total number of messages (excluding system messages)"""
        return len([msg for msg in self.messages if not msg.is_system])

    def get_date_range(self) -> tuple:
        """Get the date range of the conversation"""
        if not self.messages:
            return None, None

        timestamps = [msg.timestamp for msg in self.messages]
        return min(timestamps), max(timestamps)

    def to_text(self, include_system: bool = False) -> str:
        """Convert messages back to readable text format"""
        lines = []
        for msg in self.messages:
            if msg.is_system and not include_system:
                continue

            timestamp_str = msg.timestamp.strftime('%m/%d/%y, %I:%M %p')
            lines.append(f"{timestamp_str} - {msg.sender}: {msg.content}")

        return '\n'.join(lines)


def parse_whatsapp_chat(file_content: str) -> Dict:
    """
    Convenience function to parse WhatsApp chat and return structured data

    Args:
        file_content: Raw text content from WhatsApp export

    Returns:
        Dictionary with parsed data and metadata
    """
    parser = WhatsAppChatParser()
    messages = parser.parse(file_content)

    start_date, end_date = parser.get_date_range()

    return {
        'messages': [msg.to_dict() for msg in messages],
        'participants': parser.get_participants(),
        'message_count': parser.get_message_count(),
        'date_range': {
            'start': start_date.isoformat() if start_date else None,
            'end': end_date.isoformat() if end_date else None
        },
        'text': parser.to_text()
    }
