from plots import country_incremental_comparison, country_total_comparison

if __name__ == "__main__":
    country_names = ["United States", "Italy", "South Korea", "China", "Canada"]
    country_incremental_comparison(country_names)
    country_total_comparison(country_names)

    # country_incremental_comparison([
    #     "Italy",
    #     "United States",
    #     "South Korea",
    #     "Singapore",
    #     "China",
    #     "Iran",
    #     "United Kingdom",
    #     "Canada"])
