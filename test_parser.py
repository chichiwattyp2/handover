"""
Simple test script for WhatsApp parser
Run this to verify the parser works correctly
"""

from whatsapp_parser import parse_whatsapp_chat

def test_parser():
    """Test the WhatsApp parser with sample chat"""

    print("🧪 Testing WhatsApp Parser...\n")

    # Read sample chat
    try:
        with open('sample_chat.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ Sample chat file loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load sample chat: {e}")
        return False

    # Parse the chat
    try:
        result = parse_whatsapp_chat(content)
        print("✅ Chat parsed successfully\n")
    except Exception as e:
        print(f"❌ Failed to parse chat: {e}")
        return False

    # Display results
    print("📊 Parsing Results:")
    print("-" * 50)
    print(f"Participants: {', '.join(result['participants'])}")
    print(f"Message Count: {result['message_count']}")
    print(f"Date Range: {result['date_range']['start']} to {result['date_range']['end']}")
    print(f"Total Messages (including system): {len(result['messages'])}")

    # Show first few messages
    print("\n📝 First 3 Messages:")
    print("-" * 50)
    for i, msg in enumerate(result['messages'][:3]):
        print(f"{i+1}. [{msg['timestamp']}] {msg['sender']}: {msg['content'][:50]}...")

    print("\n✅ All tests passed!")
    return True

if __name__ == '__main__':
    test_parser()
