<p align="center">
  <img src="https://your-image-url-here.png" alt="NexaAuto Logo" width="250">
</p>

# NexaAuto - Automated Building Data Generator

🏗️ Welcome to NexaAuto, your gateway to revolutionizing building data generation! Are you a recruiter or a client in need of sophisticated automated solutions? Look no further, as NexaAuto is here to captivate your imagination and meet your project needs.

## Why NexaAuto?

NexaAuto combines the power of automation with advanced AI-driven text generation to provide you with an unrivaled building data generation experience. With NexaAuto, you can:

- 🚀 **Automate Data Gathering**: Leverage Selenium to effortlessly scrape real-time data from diverse sources.
- 📊 **Efficient Data Structuring**: Utilize the data-processing prowess of Pandas to organize information in a structured format.
- 🧠 **AI Enrichment**: Employ a reverse-engineered Bing GPT-4 model to enhance and expand text-based data.

## Data Columns

NexaAuto generates comprehensive data, including:

- ✨ **HOUSENUMBER**: Accurate house number information.
- 🚏 **PRESTREETDIR**: Precise pre-street direction data.
- 🏠 **STREETNAME**: Detailed street names.
- 🛣️ **STREETTYPE**: Categorized street types.
- 🏢 **POSTSTREETDIR**: Post-street direction details.
- 🌆 **CITY**: City data.
- 🗺️ **STATECODE**: State codes for precise location.
- 📬 **ZIP5**: Zip code information.
- 🏘️ **COMPLEX_RWID**: Complex reference IDs.
- 🏢 **UNITS_COUNT**: Count of units in each building.
- 🏛️ **BUILDINGS_COUNT**: Building count for each complex.
- 🏢 **Apartment_Availability**: Information on apartment availability.
- 🏠 **COMPLEX_NAME**: Names of apartment complexes.
- 🔗 **URL**: URLs to access the data source.
- 🏠 **Apartment_Alternate_Address**: Alternate apartment addresses.
- 💬 **Comments**: Additional comments and notes.

## Get Started

Ready to harness the power of NexaAuto for your projects? Here's how to get started:

1. **Clone the Repository**: Begin by cloning our repository to your local machine:

   ```bash
   git clone https://github.com/iamspdarsan/nexaauto.git

Explore the Code: Dive into the code, customize it to your specific needs, and kickstart your building data generation projects.

Reach Out: Have questions or need assistance? We're here to help! Feel free to open an issue or reach out to us here [darsan@cresteem.com].

Explore the Code 🚀

Let NexaAuto be your trusted partner in the world of data automation. We look forward to embarking on this exciting journey with you!


# Project Requirements and Installation

To run NexaAuto and harness its full potential, you'll need to install the following Python packages using `pip`. Make sure you have Python and `pip` installed on your system. If not, you can download Python from the [official website](https://www.python.org/downloads/), and `pip` will be included by default.

## Pandas
[Pandas](https://pandas.pydata.org/) is a powerful data manipulation and analysis library. It's essential for efficient data structuring and manipulation in NexaAuto.

**Installation:**

```bash
pip install pandas
```

## TQDM

TQDM is a fast, extensible progress bar for loops and processes. It provides real-time feedback on the progress of various tasks, making your experience with NexaAuto smoother.

**Installation:**
```bash
pip install tqdm
```

## Selenium
Selenium is a web automation tool that allows you to control web browsers through programs and perform tasks like web scraping. It's a fundamental component for data gathering in NexaAuto.

**Installation:**

```bash
pip install selenium
```

## EdgeGPT
I have used this reverse engineered BingGPT API by acheong08: <https://github.com/acheong08/EdgeGPT>

```bash
python3 -m pip install EdgeGPT --upgrade
```

Once you've installed these packages, you're ready to start using NexaAuto for your automated building data generation needs.