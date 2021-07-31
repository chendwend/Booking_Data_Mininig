from sources.source_page import *
from time import perf_counter

if __name__ == '__main__':
    start = perf_counter()
    destination = input("Enter desired destination: ")
    website = Website(WEB_SOURCE)
    website.enter_location(destination)
    website.click_search_button()
    features_list = website.get_all_features()
    website.teardown()
    time = perf_counter() - start
    print(f"\n-----------------\nExecution time: {time:.2f} seconds")
    for element in features_list[:5]:
        print(element)
