import requests
import random
import string
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import sys
import os
import platform
import re

# Global list to track taken usernames
TAKEN_USERNAMES = set()

# Function to load taken usernames from file
def load_taken_usernames(filename='taken_usernames.txt'):
    try:
        with open(filename, 'r') as file:
            return set(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        return set()

# Function to save taken usernames to file
def save_taken_usernames(filename='taken_usernames.txt'):
    try:
        with open(filename, 'w') as file:
            for username in TAKEN_USERNAMES:
                file.write(username + '\n')
    except Exception as e:
        print(f"Error saving taken usernames: {e}")

# Function to validate username against Roblox rules
def validate_roblox_username(username):
    """
    Roblox username rules:
    - 3 to 20 characters long
    - Only letters, numbers, and single underscore (_)
    - Underscore cannot be first or last character
    - No spaces, special characters, or multiple underscores in a row
    """
    # Check length
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters"
    
    # Check if starts or ends with underscore
    if username.startswith('_') or username.endswith('_'):
        return False, "Username cannot start or end with underscore"
    
    # Check for valid characters (letters, numbers, underscore)
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscore"

    # Check for multiple underscores (only one underscore allowed total in entire username)
    if username.count('_') > 1:
        return False, "Username can only contain one underscore total"
    
    # Check for multiple consecutive underscores
    if '__' in username:
        return False, "Username cannot have multiple underscores in a row"
    
    # Check for spaces (though regex above should catch this)
    if ' ' in username:
        return False, "Username cannot contain spaces"
    
    return True, "Valid username"

# Function to generate Roblox-compliant username
def generate_roblox_username(bits, schemas):
    """Generate username that follows Roblox rules"""
    max_attempts = 50
    
    for attempt in range(max_attempts):
        bit1 = random.choice(bits)
        bit2 = random.choice(bits)
        schema = random.choice(schemas)
        number = generate_random_number()
        
        try:
            username = schema.format(bit1=bit1, bit2=bit2, number=number)
            
            # Validate the generated username
            is_valid, message = validate_roblox_username(username)
            
            if is_valid and username not in TAKEN_USERNAMES:
                return username
        except (KeyError, IndexError):
            # If schema formatting fails, try another one
            continue
    
    # If we can't generate a valid one after max attempts, create a simple one
    simple_username = f"User{random.randint(10000, 99999)}"
    is_valid, message = validate_roblox_username(simple_username)
    if is_valid:
        return simple_username
    
    # Last resort - very basic username
    return f"Player{random.randint(100000, 999999)}"[:20]

# Function to read username bits from a file
def read_username_bits(file_path):
    try:
        with open(file_path, 'r') as file:
            bits = [line.strip() for line in file if line.strip()]
            # Filter bits to ensure they're valid for Roblox
            valid_bits = []
            for bit in bits:
                if re.match(r'^[a-zA-Z0-9]+$', bit) and 1 <= len(bit) <= 18:
                    valid_bits.append(bit)
            print(f"Loaded {len(valid_bits)} valid username bits")
            return valid_bits
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return []

# Function to read username schemas from a file
def read_username_schemas(file_path):
    try:
        with open(file_path, 'r') as file:
            schemas = [line.strip() for line in file if line.strip()]
            # Filter schemas to ensure they produce valid usernames
            valid_schemas = []
            for schema in schemas:
                # Check if schema has proper placeholders and reasonable length
                if '{bit1}' in schema and '{bit2}' in schema and '{number}' in schema:
                    # Test with sample data to see if it produces valid format
                    test_username = schema.format(bit1='test', bit2='user', number='123')
                    is_valid, message = validate_roblox_username(test_username)
                    if is_valid:
                        valid_schemas.append(schema)
            print(f"Loaded {len(valid_schemas)} valid username schemas")
            return valid_schemas
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return []

# Function to generate a random password
def generate_password(length=12):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Function to generate a random number
def generate_random_number():
    return str(random.randint(100, 9999))

def generate_random_birthday():
    """Generate a random birthday for someone between 18-30 years old"""
    today = datetime.now()

    # Calculate date range correctly
    # 30 years ago (oldest)
    max_birth_date = today.replace(year=today.year - 30)
    # 18 years ago (youngest)
    min_birth_date = today.replace(year=today.year - 18)

    # Generate random date between min and max
    random_days = random.randint(0, (min_birth_date - max_birth_date).days)
    random_birth_date = min_birth_date - timedelta(days=random_days)

    # Month abbreviations for Roblox dropdown
    month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    return {
        'day': random_birth_date.day,
        'month': month_abbr[random_birth_date.month - 1],
        'year': random_birth_date.year,
        'month_number': random_birth_date.month
    }

def setup_driver():
    """Setup Chrome driver"""
    options = Options()

    # Remove automation detection
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Additional stealth options
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--no-first-run')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--remote-debugging-port=0')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    # Keep browser open for debugging
    options.add_experimental_option("detach", True)

    try:
        driver = webdriver.Chrome(options=options)

        # Remove webdriver property and other automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        print("✓ Browser started successfully")
        return driver

    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        return None

def find_element_safe(driver, by, value, timeout=10):
    """Safely find element with timeout"""
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    except:
        return None

def clear_username_field(driver):
    """Clear the username field completely"""
    try:
        username_field = find_element_safe(driver, By.ID, "signup-username")
        if username_field:
            # Method 1: Click and clear using backspace
            username_field.click()
            time.sleep(0.5)
            
            # Method 2: Select all and delete
            username_field.send_keys(Keys.CONTROL + "a")
            time.sleep(0.2)
            username_field.send_keys(Keys.DELETE)
            time.sleep(0.5)
            
            # Method 3: Clear using JavaScript as backup
            driver.execute_script("arguments[0].value = '';", username_field)
            time.sleep(0.5)
            
            # Method 4: Clear using clear() method
            username_field.clear()
            time.sleep(0.5)
            
            # Click somewhere else to trigger validation
            birthday_field = find_element_safe(driver, By.ID, "DayDropdown")
            if birthday_field:
                birthday_field.click()
                time.sleep(0.5)
            
            # Verify field is empty
            current_value = username_field.get_attribute('value')
            if current_value and current_value.strip():
                print(f"⚠ Warning: Username field still contains: '{current_value}'")
                # Try one more time with force JavaScript
                driver.execute_script("arguments[0].value = ''; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", username_field)
                time.sleep(1)
            else:
                print("✓ Username field cleared successfully")
                
            return True
        return False
    except Exception as e:
        print(f"Error clearing username field: {e}")
        return False

def set_birthday_first(driver, birthday):
    """Set birthday fields first before handling username"""
    print("Setting birthday information first...")
    
    try:
        # Day dropdown
        birthday_day = find_element_safe(driver, By.ID, "DayDropdown")
        if birthday_day:
            # Convert day to string with leading zero if needed
            day_value = str(birthday['day']).zfill(2)
            Select(birthday_day).select_by_value(day_value)
            print(f"✓ Set birthday day: {birthday['day']}")
        else:
            print("✗ Could not find day dropdown")
            return False

        # Month dropdown
        birthday_month = find_element_safe(driver, By.ID, "MonthDropdown")
        if birthday_month:
            Select(birthday_month).select_by_value(birthday['month'])
            print(f"✓ Set birthday month: {birthday['month']}")
        else:
            print("✗ Could not find month dropdown")
            return False

        # Year dropdown
        birthday_year = find_element_safe(driver, By.ID, "YearDropdown")
        if birthday_year:
            Select(birthday_year).select_by_value(str(birthday['year']))
            print(f"✓ Set birthday year: {birthday['year']}")
        else:
            print("✗ Could not find year dropdown")
            return False

        # Wait a moment for birthday to register
        time.sleep(2)
        return True

    except Exception as e:
        print(f"Error setting birthday: {e}")
        return False

def check_username_available(driver, username):
    """Check if username is available by typing it and checking validation"""
    try:
        # First, clear the username field completely
        if not clear_username_field(driver):
            print("✗ Could not clear username field")
            return False

        # Find username field
        username_field = find_element_safe(driver, By.ID, "signup-username")
        if not username_field:
            return False

        # Type username slowly
        print(f"  Typing username: {username}")
        for char in username:
            username_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))

        # Wait for validation to appear
        time.sleep(3)

        # Check for error message
        validation_element = driver.find_element(By.ID, "signup-usernameInputValidation")
        if validation_element:
            validation_text = validation_element.text.lower()
            if "already in use" in validation_text or "taken" in validation_text:
                print(f"  ✗ Username '{username}' is taken (validation message)")
                # Add to taken usernames list
                TAKEN_USERNAMES.add(username)
                return False
            elif "available" in validation_text or validation_text == "":
                print(f"  ✓ Username '{username}' appears available")
                return True

        # If no clear validation, check for suggestion box (indicates taken username)
        suggestion_box = driver.find_elements(By.CLASS_NAME, "username-suggestion-container")
        if suggestion_box and suggestion_box[0].is_displayed():
            print(f"  ✗ Username '{username}' is taken (suggestion box shown)")
            TAKEN_USERNAMES.add(username)
            return False

        # Check if signup button is enabled (indicates valid form)
        signup_button = find_element_safe(driver, By.ID, "signup-button")
        if signup_button and signup_button.is_enabled():
            print(f"  ✓ Username '{username}' appears available (signup button enabled)")
            return True

        # If we get here and button is disabled, username might be taken
        if signup_button and not signup_button.is_enabled():
            print(f"  ✗ Username '{username}' might be taken (signup button disabled)")
            TAKEN_USERNAMES.add(username)
            return False

        print(f"  ? Username '{username}' - unclear status, assuming available")
        return True  # Default to available if we can't determine

    except Exception as e:
        print(f"Error checking username availability: {e}")
        return True  # Assume available if we can't check

def wait_for_captcha_and_continue():
    """Wait for user to complete CAPTCHA and press Enter"""
    print("\n" + "="*60)
    print("⚠ CAPTCHA REQUIRED")
    print("="*60)
    print("Please complete the CAPTCHA in the browser window.")
    print("After you successfully complete the CAPTCHA,")
    print("come back here and press Enter to continue...")
    print("="*60)
    input("Press Enter after CAPTCHA is completed...")
    print("✓ Continuing with account creation...")

def create_account_selenium(username, password, driver, birthday):
    """Create account using Selenium for the CreateAccount page"""
    try:
        print(f"Generated birthday: {birthday['month']} {birthday['day']}, {birthday['year']} (Age: {datetime.now().year - birthday['year']} years)")

        # Go directly to the CreateAccount page
        print("Loading Roblox Create Account page...")
        driver.get("https://www.roblox.com/CreateAccount")

        # Wait for page to load completely
        time.sleep(5)

        print("Looking for form elements on CreateAccount page...")

        # SET BIRTHDAY FIRST
        if not set_birthday_first(driver, birthday):
            print("✗ Failed to set birthday. Cannot proceed.")
            return False

        # Now check if username is available
        print(f"Checking if username '{username}' is available...")
        if not check_username_available(driver, username):
            print(f"✗ Username '{username}' is already taken. Skipping...")
            return False
        print(f"✓ Username '{username}' appears to be available")

        # Find username field again (page might have refreshed validation)
        username_field = find_element_safe(driver, By.ID, "signup-username")
        if not username_field:
            print("✗ Could not find username field after validation")
            return False

        # Find password field
        password_field = find_element_safe(driver, By.ID, "signup-password")
        if not password_field:
            print("✗ Could not find password field")
            return False

        # Fill the form
        print("Filling username and password...")

        # Clear and fill username (again to ensure it's set)
        if not clear_username_field(driver):
            print("⚠ Could not clear username field before final fill")
        
        for char in username:
            username_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))

        # Clear and fill password
        password_field.clear()
        for char in password:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))

        # Select gender (Male) - optional, can skip if not found
        print("Selecting gender...")
        gender_male = find_element_safe(driver, By.ID, "MaleButton")
        if gender_male:
            gender_male.click()
            print("✓ Selected gender")
        else:
            print("⚠ Gender selection not found, continuing without...")

        # Wait a moment for form validation
        time.sleep(3)

        # Look for signup button and check if it's enabled
        signup_button = find_element_safe(driver, By.ID, "signup-button")
        if not signup_button:
            signup_button = find_element_safe(driver, By.CSS_SELECTOR, "button[type='submit']")
        if not signup_button:
            signup_button = find_element_safe(driver, By.XPATH, "//button[contains(text(), 'Sign Up')]")

        if not signup_button:
            print("✗ Could not find signup button")
            driver.save_screenshot("debug_signup_button.png")
            return False

        # Check if button is enabled
        if not signup_button.is_enabled():
            print("✗ Signup button is disabled. Checking possible issues...")
            
            # Check for specific error messages
            validation_element = driver.find_element(By.ID, "signup-usernameInputValidation")
            if validation_element and validation_element.text:
                print(f"  Username validation: {validation_element.text}")
            
            password_validation = driver.find_element(By.ID, "signup-passwordInputValidation")
            if password_validation and password_validation.text:
                print(f"  Password validation: {password_validation.text}")
            
            # Try to trigger validation by clicking away
            username_field.click()
            time.sleep(1)
            
            if not signup_button.is_enabled():
                print("  Signup button still disabled after validation check")
                return False

        print("✓ Found enabled signup button")
        print("Form filled successfully!")

        # Check if there's a CAPTCHA before clicking signup
        captcha_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='captcha'], [class*='g-recaptcha'], iframe[src*='recaptcha']")
        if captcha_elements:
            wait_for_captcha_and_continue()

        print("Attempting to create account...")
        
        # Scroll to button and click
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", signup_button)
        time.sleep(1)
        signup_button.click()

        # Wait for account creation
        print("Waiting for account creation result...")
        success = False

        for check in range(15):  # Check for 45 seconds total
            time.sleep(3)

            # Check for success indicators
            current_url = driver.current_url.lower()
            page_source = driver.page_source.lower()

            success_indicators = [
                "home" in current_url,
                "welcome" in current_url,
                "www.roblox.com/home" in current_url,
                current_url == "https://www.roblox.com/",
                "success" in page_source,
                "my-account" in current_url,
                "user" in current_url,
                "dashboard" in current_url,
                "profile" in current_url
            ]

            if any(success_indicators):
                print("✓ Account creation successful!")
                success = True
                break

            # Check for error messages
            error_indicators = [
                "username is already in use",
                "invalid password",
                "error occurred",
                "something went wrong",
                "unable to create account",
                "please try again",
                "captcha",
                "verification"
            ]

            for error in error_indicators:
                if error in page_source:
                    print(f"✗ Error detected: {error}")
                    return False

            print(f"  Still waiting... ({check + 1}/15)")

        if not success:
            print("⚠ Could not automatically detect success, checking manually...")
            print(f"Current URL: {driver.current_url}")
            
            # Let user manually check
            print("\nPlease check the browser window:")
            print("1. Is there a success message?")
            print("2. Are you logged in?")
            print("3. Are you on the Roblox home page?")
            confirm = input("Did the account creation succeed? (y/n): ").lower().strip()

            if confirm in ['y', 'yes']:
                return True
            else:
                return False

        return True

    except Exception as e:
        print(f"Selenium error: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot(f"error_{username}.png")
        return False

# Function to save created accounts to a file
def save_account(username, password, birthday, filename='created_accounts.txt'):
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(f"Username: {username}\n")
            file.write(f"Password: {password}\n")
            file.write(f"Birthday: {birthday['month']} {birthday['day']}, {birthday['year']}\n")
            file.write(f"Age: {datetime.now().year - birthday['year']} years\n")
            file.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 50 + "\n")
        print(f"✓ Account details saved to {filename}")
    except Exception as e:
        print(f"Error saving account to file: {e}")

def get_available_username(driver, bits, schemas, max_attempts=10):
    """Generate and check for available username"""
    for attempt in range(max_attempts):
        username = generate_roblox_username(bits, schemas)
        print(f"Checking username {attempt + 1}/{max_attempts}: {username}")
        
        # Validate username before testing
        is_valid, message = validate_roblox_username(username)
        if not is_valid:
            print(f"  ✗ Invalid username: {message}")
            continue
            
        if check_username_available(driver, username):
            return username
        print(f"  Username taken, trying another...")
    
    return None

# Main function
def main():
    print("=== Roblox Account Creator ===")
    print("Using: https://www.roblox.com/CreateAccount")
    print("Strategy: Set birthday FIRST, then find available username")
    print("Features: Roblox username validation, CAPTCHA handling, username caching")
    print("Roblox Username Rules:")
    print("  - 3-20 characters")
    print("  - Letters, numbers, single underscore only")
    print("  - No spaces or special characters")
    print("  - Underscore cannot be first/last character")
    print("\nNote: This tool requires manual CAPTCHA solving.")
    print("Make sure you have permission to create accounts for testing.\n")

    # Load taken usernames from previous sessions
    global TAKEN_USERNAMES
    TAKEN_USERNAMES = load_taken_usernames()
    print(f"Loaded {len(TAKEN_USERNAMES)} known taken usernames from cache")

    # Load username data
    bits = read_username_bits('username_bits.txt')
    schemas = read_username_schemas('username_schemas.txt')

    if not bits or not schemas:
        print("Error: Could not load username bits or schemas files.")
        print("Please create these files:")
        print("username_bits.txt - list of word parts (e.g., dark, light, fire, water)")
        print("username_schemas.txt - list of templates (e.g., {bit1}{bit2}{number}, {bit1}_{bit2}{number})")
        return

    # Get number of accounts to create
    try:
        num_accounts = int(input("Enter the number of accounts to create: "))
        if num_accounts <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    print(f"\nCreating {num_accounts} accounts...")

    successful_creations = 0
    drivers = []

    try:
        for i in range(num_accounts):
            print(f"\n" + "="*50)
            print(f"Attempt {i+1}/{num_accounts}")
            print("="*50)

            # Generate birthday first
            birthday = generate_random_birthday()
            print(f"Generated birthday: {birthday['month']} {birthday['day']}, {birthday['year']} (Age: {datetime.now().year - birthday['year']} years)")

            # Setup driver
            driver = setup_driver()
            if not driver:
                print("Failed to setup browser. Exiting.")
                break

            drivers.append(driver)

            # Go to signup page
            driver.get("https://www.roblox.com/CreateAccount")
            time.sleep(5)

            # SET BIRTHDAY FIRST
            if not set_birthday_first(driver, birthday):
                print("✗ Failed to set birthday, skipping this attempt...")
                continue

            # Now find available username
            username = get_available_username(driver, bits, schemas)
            if not username:
                print("✗ Could not find an available username after multiple attempts")
                continue

            password = generate_password()

            print(f"✓ Available Username: {username}")
            print(f"✓ Password: {password}")

            if create_account_selenium(username, password, driver, birthday):
                print(f"🎉 SUCCESS: Account '{username}' created!")
                save_account(username, password, birthday)
                successful_creations += 1
            else:
                print(f"❌ FAILED: Could not create account '{username}'")

            # Add delay between attempts and wait for CAPTCHA if needed
            if i < num_accounts - 1:
                wait_time = random.randint(15, 30)
                print(f"\nWaiting {wait_time} seconds before next attempt...")
                
                # Check if CAPTCHA might be needed for next attempt
                print("If you see a CAPTCHA in the browser, complete it now.")
                print("The script will continue automatically after the wait time.")
                time.sleep(wait_time)
                
                # Ask user to confirm CAPTCHA is done if needed
                print("\nIf there was a CAPTCHA, please ensure it's completed.")
                input("Press Enter to continue to the next account creation...")

    except KeyboardInterrupt:
        print("\n⏹ Process interrupted by user")
    finally:
        # Save taken usernames before closing
        save_taken_usernames()
        print(f"✓ Saved {len(TAKEN_USERNAMES)} taken usernames to cache")

        # Keep browsers open until user confirms
        if drivers:
            print(f"\nAll account creation attempts completed.")
            print(f"Keeping {len(drivers)} browser window(s) open for verification...")
            input("Press Enter when you're ready to close all browser windows...")

            for driver in drivers:
                try:
                    driver.quit()
                except:
                    pass
            print("All browser windows closed.")

    print(f"\n" + "="*50)
    print("CREATION SUMMARY")
    print("="*50)
    print(f"✅ Successful: {successful_creations}")
    print(f"❌ Failed: {num_accounts - successful_creations}")
    print(f"📁 Accounts saved to: created_accounts.txt")
    print(f"📁 Taken usernames saved to: taken_usernames.txt")

if __name__ == "__main__":
    main()
