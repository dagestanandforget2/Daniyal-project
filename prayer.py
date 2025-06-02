import requests

def get_prayer_times(city, country, madhab):
    api_url = "https://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": city,
        "country": country,
        "method": 2,  # ISNA Calculation Method
        "school": madhab 
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "timings" in data["data"]:
            return data["data"]["timings"]
        else:
            print("Error: Unexpected response format from Aladhan API.")
            return None
    else:
        print(f"Error fetching prayer times: {response.status_code}")
        return None
def main():
    city = input("Enter your city: ").strip()
    country = input("Enter your country: ").strip()
    madhab = input("Enter your madhab (0 for Shafi/Hanbali/Maliki, 1 for Hanafi): ").strip()

    # Validate madhab input
    if madhab not in ["0", "1"]:
        print("Invalid input for madhab. Please enter 0 for Shafi or 1 for Hanafi.")
        return

    prayer_times = get_prayer_times(city, country, madhab)
    
    if prayer_times:
        print(f"\nPrayer times for {city}, {country}:")
        for prayer, time in prayer_times.items():
            print(f"{prayer}: {time}")

if __name__ == "__main__":
    main()