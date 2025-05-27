import datasets

def load_dataset():
    dataset = datasets.load_dataset("lavita/ChatDoctor-HealthCareMagic-100k", split = "train")
    return dataset.select(range(1000))