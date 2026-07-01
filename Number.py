import os
import random
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# === CONFIG ===
SAVE_DIR = r"/home/chest/Documents/Number Verifiy tools/Valid Number/"
os.makedirs(SAVE_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(SAVE_DIR, "history.txt")
OUTPUT_FILE = os.path.join(SAVE_DIR, "MobileNumbers.txt")

# === MOBILE ONLY COUNTRY DATA ===
COUNTRY_DATA = {
    "USA": {
        "country_code": "+1",
        "area_codes": {
            "Alabama": ["205", "251", "256", "334", "938"],
            "Alaska": ["907"],
            "Arizona": ["480", "520", "602", "623", "928"],
            "Arkansas": ["479", "501", "870"],
            "California": ["209", "213", "279", "310", "323", "408", "415", "424", "442", "510", "530", "559", "562", "619", "626", "628", "650", "657", "661", "669", "707", "714", "747", "760", "805", "818", "820", "831", "858", "909", "916", "925", "949", "951"],
            "Colorado": ["303", "719", "720", "970"],
            "Connecticut": ["203", "475", "860", "959"],
            "Florida": ["239", "305", "321", "352", "386", "407", "561", "727", "754", "772", "786", "813", "850", "863", "904", "941", "954"],
            "Georgia": ["229", "404", "470", "478", "678", "706", "762", "770", "912"],
            "Idaho": ["208", "986"],
            "Illinois": ["217", "224", "309", "312", "331", "618", "630", "708", "773", "779", "815", "847", "872"],
            "Indiana": ["219", "260", "317", "463", "574", "765", "812", "930"],
            "Iowa": ["319", "515", "563", "641", "712"],
            "Kansas": ["316", "620", "785", "913"],
            "Kentucky": ["270", "364", "502", "606", "859"],
            "Louisiana": ["225", "318", "337", "504", "985"],
            "Maryland": ["240", "301", "410", "443", "667"],
            "Massachusetts": ["339", "351", "413", "508", "617", "774", "781", "857", "978"],
            "Michigan": ["231", "248", "269", "313", "517", "586", "616", "734", "810", "906", "947", "989"],
            "Minnesota": ["218", "320", "507", "612", "651", "763", "952"],
            "Mississippi": ["228", "601", "662", "769"],
            "Missouri": ["314", "417", "573", "636", "660", "816"],
            "Nebraska": ["308", "402", "531"],
            "Nevada": ["702", "725", "775"],
            "New Jersey": ["201", "551", "609", "640", "732", "848", "856", "862", "908", "973"],
            "New York": ["212", "315", "332", "347", "516", "518", "585", "607", "631", "646", "680", "716", "718", "838", "845", "914", "917", "929", "934"],
            "North Carolina": ["252", "336", "704", "743", "828", "910", "919", "980", "984"],
            "Ohio": ["216", "220", "234", "330", "380", "419", "440", "513", "567", "614", "740", "937"],
            "Oklahoma": ["405", "539", "580", "918"],
            "Oregon": ["458", "503", "541", "971"],
            "Pennsylvania": ["215", "223", "267", "272", "412", "445", "484", "570", "610", "717", "724", "814", "878"],
            "South Carolina": ["803", "843", "854", "864"],
            "Tennessee": ["423", "615", "629", "731", "865", "901", "931"],
            "Texas": ["210", "214", "254", "281", "325", "346", "361", "409", "430", "432", "469", "512", "682", "713", "726", "737", "806", "817", "830", "832", "903", "915", "936", "940", "945", "956", "972", "979"],
            "Utah": ["385", "435", "801"],
            "Virginia": ["276", "434", "540", "571", "703", "757", "804"],
            "Washington": ["206", "253", "360", "425", "509", "564"],
            "Wisconsin": ["262", "274", "414", "534", "608", "715", "920"],
        }
    },
    "Canada": {
        "country_code": "+1",
        "area_codes": {
            "Alberta": ["403", "587", "780", "825"],
            "British Columbia": ["236", "250", "604", "672", "778"],
            "Manitoba": ["204", "431"],
            "New Brunswick": ["506"],
            "Newfoundland": ["709"],
            "Nova Scotia": ["782", "902"],
            "Ontario": ["226", "249", "289", "343", "365", "416", "437", "519", "548", "613", "647", "705", "807", "905"],
            "Quebec": ["367", "418", "438", "450", "514", "579", "581", "819", "873"],
            "Saskatchewan": ["306", "639"],
        }
    },
    "Australia": {
        "country_code": "+61",
        "area_codes": {
            "Mobile": ["04"]
        }
    },
    "UK": {
        "country_code": "+44",
        "area_codes": {
            "Mobile": ["07"]
        }
    }
}

write_lock = threading.Lock()

# === UTILITIES ===
def load_history():
    existing = set()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    existing.add(line)
    return existing

def append_to_history(new_numbers):
    with write_lock:
        with open(HISTORY_FILE, "a") as f:
            for num in sorted(new_numbers):
                f.write(num + "\n")

def save_numbers(numbers_with_states):
    with write_lock:
        with open(OUTPUT_FILE, "w") as f:
            f.write(f"Total mobile numbers: {len(numbers_with_states)}\nGenerated on {datetime.now()}\n\n")
            for num, state in sorted(numbers_with_states):
                f.write(f"{num} ---- {state}\n")
    return OUTPUT_FILE

# === MOBILE NUMBER GENERATORS ===
def generate_usa_mobile():
    state = random.choice(list(COUNTRY_DATA["USA"]["area_codes"].keys()))
    area_code = random.choice(COUNTRY_DATA["USA"]["area_codes"][state])

    exchange = str(random.randint(2, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    subscriber = ''.join(str(random.randint(0, 9)) for _ in range(4))
    local_number = area_code + exchange + subscriber
    full_number = COUNTRY_DATA["USA"]["country_code"] + " " + local_number
    return (full_number, state)

def generate_canada_mobile():
    province = random.choice(list(COUNTRY_DATA["Canada"]["area_codes"].keys()))
    area_code = random.choice(COUNTRY_DATA["Canada"]["area_codes"][province])
    exchange = str(random.randint(2, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    subscriber = ''.join(str(random.randint(0, 9)) for _ in range(4))
    local_number = area_code + exchange + subscriber
    full_number = COUNTRY_DATA["Canada"]["country_code"] + " " + local_number
    return (full_number, province)

def generate_australia_mobile():
    prefix = "04"
    remaining = ''.join(str(random.randint(0, 9)) for _ in range(8))
    local_number = prefix + remaining
    full_number = COUNTRY_DATA["Australia"]["country_code"] + " " + local_number[1:]
    return (full_number, "Mobile")

def generate_uk_mobile():
    prefix = "07"
    remaining = ''.join(str(random.randint(0, 9)) for _ in range(9))
    local_number = prefix + remaining
    full_number = COUNTRY_DATA["UK"]["country_code"] + " " + local_number[1:]
    return (full_number, "Mobile")

def generate_number(country):
    if country == "USA":
        return generate_usa_mobile()
    elif country == "Canada":
        return generate_canada_mobile()
    elif country == "Australia":
        return generate_australia_mobile()
    elif country == "UK":
        return generate_uk_mobile()
    else:
        raise ValueError("Unsupported country")

# === MAIN ===
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("="*55)
    print("     MOBILE NUMBER GENERATOR (Cell Phone Only)")
    print("="*55)
    print("Generates realistic mobile phone numbers for USA, Canada, Australia, and UK.")
    print("Only cell phone numbers (no landlines).\n")

    countries = ["USA", "Canada", "Australia", "UK"]
    for i, c in enumerate(countries, 1):
        print(f"{i}. {c}")

    while True:
        try:
            choice = int(input("\nSelect country (1-4): "))
            if 1 <= choice <= 4:
                break
            else:
                print("Choose a number from 1 to 4.")
        except:
            print("Invalid input.")

    country = countries[choice-1]

    while True:
        try:
            amount = int(input("How many unique mobile numbers to generate? (1-100000): "))
            if 1 <= amount <= 100000:
                break
            else:
                print("Enter a number between 1 and 100000.")
        except:
            print("Invalid input.")

    print("\nLoading previously generated numbers from history...")
    existing_numbers = load_history()
    print(f"{len(existing_numbers)} existing numbers loaded.")
    print(f"\nGenerating {amount} mobile numbers for {country}...")

    new_numbers = set()
    new_numbers_with_states = []

    def generate_worker(target_count):
        local_new = set()
        local_new_with_states = []
        attempts = 0
        while len(local_new) < target_count and attempts < target_count * 10:
            num, state = generate_number(country)
            with write_lock:
                if num not in existing_numbers and num not in new_numbers and num not in local_new:
                    local_new.add(num)
                    local_new_with_states.append((num, state))
            attempts += 1
        with write_lock:
            new_numbers.update(local_new)
            new_numbers_with_states.extend(local_new_with_states)

    max_workers = 10
    base = amount // max_workers
    remainder = amount % max_workers

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(max_workers):
            count = base + (1 if i < remainder else 0)
            futures.append(executor.submit(generate_worker, count))
        for f in futures:
            f.result()

    print(f"\nGenerated {len(new_numbers)} new unique mobile numbers.")
    save_path = save_numbers(new_numbers_with_states)
    print(f"Saved to: {save_path}")
    append_to_history(new_numbers)

    print("\nSample of generated mobile numbers:")
    sample_count = min(10, len(new_numbers_with_states))
    for num, state in new_numbers_with_states[:sample_count]:
        print(f"{num} ---- {state}")

    print("\nOperation completed successfully!")

if __name__ == "__main__":
    main()
