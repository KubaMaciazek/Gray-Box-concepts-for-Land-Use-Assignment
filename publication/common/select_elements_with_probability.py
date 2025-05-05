import random


def select_elements_with_probability(elements, prob):
    selected_elements = []
    discarded_elements = []

    for element in elements:
        if random.random() < prob:
            selected_elements.append(element)
        else:
            discarded_elements.append(element)

    return selected_elements, discarded_elements


# # Example usage
# elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# prob = 0.4
# selected, discarded = select_elements_with_probability(elements, prob)
#
# print("Selected elements:", selected)
# print("Discarded elements:", discarded)
