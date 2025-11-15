"""
AI Analyzer Module
Uses Claude AI to analyze WhatsApp conversations
"""

import os
from typing import Dict, List
from anthropic import Anthropic
import json


class WhatsAppAIAnalyzer:
    """Uses Claude AI to analyze WhatsApp conversations"""

    def __init__(self, api_key: str = None):
        """
        Initialize the AI analyzer

        Args:
            api_key: Anthropic API key (if not provided, reads from environment)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = Anthropic(api_key=self.api_key)

    def analyze_conversation(self, chat_text: str, participants: List[str]) -> Dict:
        """
        Analyze WhatsApp conversation for summary, sentiment, and actionables

        Args:
            chat_text: Formatted chat text
            participants: List of participant names

        Returns:
            Dictionary containing analysis results
        """
        # Prepare the analysis prompt
        prompt = self._create_analysis_prompt(chat_text, participants)

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.3,  # Lower temperature for more consistent analysis
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse the response
            response_text = message.content[0].text

            # Extract JSON from the response
            analysis = self._parse_analysis_response(response_text)

            return {
                'success': True,
                'analysis': analysis
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _create_analysis_prompt(self, chat_text: str, participants: List[str]) -> str:
        """Create the analysis prompt for Claude"""

        participants_str = ", ".join(participants)

        prompt = f"""You are analyzing a WhatsApp conversation between {participants_str}.

Please analyze this conversation and provide:

1. **Summary**: A concise 2-3 paragraph summary of the conversation covering main topics and key points
2. **Sentiment Analysis**: Overall sentiment (positive/negative/neutral/mixed) with a confidence score and brief explanation
3. **Individual Sentiments**: Sentiment for each participant
4. **Key Topics**: Main topics discussed (as a list)
5. **Actionables**: Extract any action items, tasks, commitments, or things that need to be done. Include:
   - What needs to be done
   - Who is responsible (if mentioned)
   - Deadline (if mentioned)
   - Priority indicators (if any)
   - Context

Return your analysis in the following JSON format:

{{
  "summary": "Your detailed summary here...",
  "overall_sentiment": {{
    "sentiment": "positive|negative|neutral|mixed",
    "confidence": 0.85,
    "explanation": "Brief explanation of the sentiment"
  }},
  "participant_sentiments": [
    {{
      "participant": "Name",
      "sentiment": "positive|negative|neutral",
      "explanation": "Brief explanation"
    }}
  ],
  "key_topics": [
    "Topic 1",
    "Topic 2"
  ],
  "actionables": [
    {{
      "action": "What needs to be done",
      "assignee": "Who (or 'Not specified')",
      "deadline": "When (or 'Not specified')",
      "priority": "high|medium|low|not specified",
      "context": "Brief context from the conversation",
      "mentioned_at": "Approximate timestamp or 'recent' for latest"
    }}
  ],
  "conversation_insights": {{
    "tone": "formal|informal|casual|professional",
    "engagement_level": "high|medium|low",
    "key_points": ["Point 1", "Point 2"]
  }}
}}

Here is the WhatsApp conversation to analyze:

---START CONVERSATION---
{chat_text}
---END CONVERSATION---

Provide your analysis in valid JSON format only, no additional text."""

        return prompt

    def _parse_analysis_response(self, response_text: str) -> Dict:
        """Parse Claude's response and extract JSON"""

        # Try to find JSON in the response
        try:
            # First, try to parse the entire response as JSON
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from markdown code blocks
            import re

            # Look for JSON in code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))

            # Look for JSON without code blocks
            json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))

            # If all parsing fails, return a structured error
            return {
                'summary': response_text[:500] + '...' if len(response_text) > 500 else response_text,
                'overall_sentiment': {
                    'sentiment': 'neutral',
                    'confidence': 0.5,
                    'explanation': 'Could not parse structured analysis'
                },
                'participant_sentiments': [],
                'key_topics': [],
                'actionables': [],
                'conversation_insights': {
                    'tone': 'unknown',
                    'engagement_level': 'unknown',
                    'key_points': []
                }
            }

    def quick_summary(self, chat_text: str) -> str:
        """
        Get a quick summary of the conversation without full analysis

        Args:
            chat_text: Formatted chat text

        Returns:
            Summary string
        """
        prompt = f"""Provide a brief 2-3 sentence summary of this WhatsApp conversation:

{chat_text[:3000]}

Be concise and focus on the main points."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return message.content[0].text

        except Exception as e:
            return f"Error generating summary: {str(e)}"
