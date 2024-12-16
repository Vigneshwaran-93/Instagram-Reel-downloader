import instaloader
import pandas as pd
import time
import os

def download_instagram_reels(csv_file):
    # Create an Instaloader instance
    loader = instaloader.Instaloader()

    # Read CSV file containing Instagram URLs
    df = pd.read_csv(csv_file)
    
    # Create a list to store results (URLs and associated content)
    reel_data = []

    # Iterate through all the URLs in the CSV file
    for idx, row in df.iterrows():
        reel_url = row['URL']
        print(f"Processing Reel {idx + 1} from URL: {reel_url}")
        
        # Extract the shortcode from the URL
        shortcode = reel_url.split("/")[-2]

        try:
            # Get the post using the shortcode
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            # Check if the post is a video (Reel)
            if post.is_video:
                print(f"Downloading Reel {idx + 1}...")
                
                # Create a folder named "Reel {idx + 1}"
                folder_name = f"Reel_{idx + 1}"
                os.makedirs(folder_name, exist_ok=True)
                
                # Download the post into the folder
                loader.download_post(post, target=folder_name)

                # Get the caption/text of the Reel
                caption = post.caption if post.caption else "No caption"

                # Store the URL and the content (caption) in the list
                reel_data.append([reel_url, caption])

                # Wait for 5 seconds before processing the next URL
                time.sleep(3)

            else:
                print(f"URL {reel_url} is not a valid Reel.")

        except Exception as e:
            print(f"Error downloading Reel from {reel_url}: {e}")
            continue

    # Create a DataFrame from the collected data
    result_df = pd.DataFrame(reel_data, columns=["Reel URL", "Content"])

    # Save the result to an Excel file
    result_df.to_excel("Reels_Information.xlsx", index=False)

    print(f"All Reels processed. Data saved to Reels_Information.xlsx.")

if __name__ == "__main__":
    # Specify the CSV file containing the Instagram URLs
    csv_file = input("Enter the path to the CSV file containing Instagram URLs: ")
    
    # Call the function to download and process Reels
    download_instagram_reels(csv_file)
