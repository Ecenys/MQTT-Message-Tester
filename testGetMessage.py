testTopic = "test/test2/test3/test4"


def search_topic(topic):
    topic_list = topic.split("/")
    message_topic_list = testTopic.split("/")
    if len(topic_list) <= len(message_topic_list):
        for i in range(len(topic_list)):
            if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
                if i == len(message_topic_list) - 1:
                    return True
            elif topic_list[i] == "#":
                return True
            else:
                return False
    return False

#main
if __name__ == "__main__":
    print("Test 1")
    print(str(search_topic("test/test2/test3/test4") == True) + "\n")
    print("Test 2")
    print(str(search_topic("test/test2/test3/test4/test5") == False) + "\n")
    print("Test 3")
    print(str(search_topic("test/test2/test3") == False) + "\n")
    print("Test 4")
    print(str(search_topic("test/+/test3/test4") == True) + "\n")
    print("Test 5")
    print(str(search_topic("test/+/test3/#") == True) + "\n")
    print("Test 6")
    print(str(search_topic("test/+/test3") == False) + "\n")
    print("Test 7")
    print(str(search_topic("test/+/test3/test4/test5") == False) + "\n")
    print("Test 8")
    print(str(search_topic("test/#") == True) + "\n")
    print("Test 9")
    print(str(search_topic("test/test2/#") == True) + "\n")
    print("Test 10")
    print(str(search_topic("test/test2/test3/#") == True) + "\n")
    print("Test 11")
    print(str(search_topic("test/test2/test3/test4/#") == False) + "\n")
    print("Test 12")
    print(str(search_topic("test/test2/test3/test4/test5/#") == False) + "\n")
    print("Test 13")
    print(str(search_topic("test/test3/test3/test4") == False) + "\n")
    