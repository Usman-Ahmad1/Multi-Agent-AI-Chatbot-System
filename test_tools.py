"""
Test the new tools in the Tools class.
"""

from src.tools import Tools

def test_tools():
    """Test all tools."""
    
    print("🔧 Testing Tools")
    print("=" * 50)
    
    # Initialize tools
    tools = Tools()
    print("✅ Tools initialized!")
    
    # 1. Test Calculator
    print("\n" + "=" * 50)
    print("🧮 Testing Calculator:")
    print("-" * 30)
    result = tools.calculate("15 * 30")
    print(f"15 * 30 = {result}")
    
    result = tools.calculate("100 / 4")
    print(f"100 / 4 = {result}")
    
    result = tools.calculate("2^10")
    print(f"2^10 = {result}")
    
    # 2. Test YouTube Search
    print("\n" + "=" * 50)
    print("📺 Testing YouTube Search:")
    print("-" * 30)
    result = tools.youtube_search("Python programming tutorial")
    print(result[:500] + "...\n")
    
    # 3. Test Web Search (Improved)
    print("\n" + "=" * 50)
    print("🌐 Testing Web Search:")
    print("-" * 30)
    result = tools.web_search("capital of France")
    print(result[:500] + "...\n")
    
    # 4. Test Read Webpage
    print("\n" + "=" * 50)
    print("📄 Testing Read Webpage:")
    print("-" * 30)
    result = tools.read_webpage("https://en.wikipedia.org/wiki/Python_(programming_language)")
    print(result[:500] + "...\n")
    
    # 5. Test List Files
    print("\n" + "=" * 50)
    print("📁 Testing List Files:")
    print("-" * 30)
    result = tools.list_files()
    print(result)
    
    # 6. Test Write File
    print("\n" + "=" * 50)
    print("✏️ Testing Write File:")
    print("-" * 30)
    result = tools.write_file("test.txt", "Hello, this is a test file!")
    print(result)
    
    # 7. Test Read File
    print("\n" + "=" * 50)
    print("📖 Testing Read File:")
    print("-" * 30)
    result = tools.read_file("test.txt")
    print(result)
    
    # 8. Test Weather (if API key is set)
    print("\n" + "=" * 50)
    print("🌤️ Testing Weather API:")
    print("-" * 30)
    result = tools.get_weather("London")
    print(result)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    test_tools()