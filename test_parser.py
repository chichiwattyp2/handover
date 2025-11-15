"""
Simple test script for WhatsApp parser
Run this to verify the parser works correctly
"""

from whatsapp_parser import parse_whatsapp_chat

def test_parser():
    """Test the WhatsApp parser with sample chat"""

    print("🧪 Testing WhatsApp Parser...\n")
    all_passed = True

    # Test 1: Original sample format
    print("=" * 60)
    print("TEST 1: Original sample format (MM/DD/YY)")
    print("=" * 60)
    try:
        with open('sample_chat.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ Sample chat file loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load sample chat: {e}")
        all_passed = False

    if all_passed:
        try:
            result = parse_whatsapp_chat(content)
            print("✅ Chat parsed successfully\n")

            print("📊 Parsing Results:")
            print("-" * 50)
            print(f"Participants: {', '.join(result['participants'])}")
            print(f"Message Count: {result['message_count']}")
            print(f"Date Range: {result['date_range']['start']} to {result['date_range']['end']}")
            print(f"Total Messages (including system): {len(result['messages'])}")

            if result['message_count'] > 0:
                print("\n📝 First 3 Messages:")
                print("-" * 50)
                for i, msg in enumerate(result['messages'][:3]):
                    print(f"{i+1}. [{msg['timestamp']}] {msg['sender']}: {msg['content'][:50]}...")
                print("✅ Test 1 PASSED\n")
            else:
                print("❌ Test 1 FAILED: No messages parsed")
                all_passed = False
        except Exception as e:
            print(f"❌ Failed to parse chat: {e}")
            all_passed = False

    # Test 2: Real format (YYYY/MM/DD)
    print("\n" + "=" * 60)
    print("TEST 2: Real WhatsApp format (YYYY/MM/DD)")
    print("=" * 60)
    try:
        with open('test_real_format.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ Real format file loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load real format file: {e}")
        all_passed = False

    if all_passed or True:  # Continue even if test 1 failed
        try:
            result = parse_whatsapp_chat(content)
            print("✅ Chat parsed successfully\n")

            print("📊 Parsing Results:")
            print("-" * 50)
            print(f"Participants: {', '.join(result['participants'])}")
            print(f"Message Count: {result['message_count']}")
            print(f"Date Range: {result['date_range']['start']} to {result['date_range']['end']}")
            print(f"Total Messages (including system): {len(result['messages'])}")

            if result['message_count'] > 0:
                print("\n📝 First 5 Messages:")
                print("-" * 50)
                for i, msg in enumerate(result['messages'][:5]):
                    sender = msg['sender'][:25] + '...' if len(msg['sender']) > 25 else msg['sender']
                    content = msg['content'][:60] + '...' if len(msg['content']) > 60 else msg['content']
                    content = content.replace('\n', ' ')
                    print(f"{i+1}. [{msg['timestamp'][:19]}] {sender}: {content}")
                print("✅ Test 2 PASSED\n")
            else:
                print("❌ Test 2 FAILED: No messages parsed")
                all_passed = False
        except Exception as e:
            print(f"❌ Failed to parse real format chat: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")
    print("=" * 60)

    return all_passed

if __name__ == '__main__':
    test_parser()
