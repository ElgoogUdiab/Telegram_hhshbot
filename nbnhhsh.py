import requests
import re
import copy

API_URL = 'https://lab.magiconch.com/api/nbnhhsh/guess'

def query(word):
    text = ",".join(re.findall(r'[a-zA-Z0-9]+', word))

    # Not making a query anyway
    if not text:
        return None
    
    r = requests.post(API_URL, data={"text": text})
    query_result = r.json()

    # return results
    results = []
    for result in query_result:
        key = result["name"]
        if "trans" in result:
            # trans
            values = result["trans"]
            result_type = "trans"
        elif "inputting" in result:
            values = result["inputting"]
            result_type = "inputting"
        results.append({
            "word": key,
            "type": result_type,
            "values": values
        })
    return results

def stringify(query_results):
    query_results = copy.deepcopy(query_results)
    results = []
    if len(query_results) == 1:
        result = query_results[0]
        # check result valid
        if not ("word" in result and "type" in result and "values" in result and\
                result["type"] in {"trans", "inputting"}):
            raise ValueError("Invalid input.", result)

        word = result["word"]
        result_type = result["type"]
        values = result["values"]

        if not values:
            results.append({
                "title": "找不到相关结果",
                "description": f"您要是知道 {word} 指什么，可以前往 https://lab.magiconch.com/nbnhhsh/ 提交结果",
                "message_to_send": f"未找到 {word} 指什么。如果您知道 {word} 指什么，可以前往 https://lab.magiconch.com/nbnhhsh/ 提交结果。"
            })
            return results
        else:
            if len(values) == 1:
                # The result:
                results.append({
                    "title": f"{word} 可能指的是：",
                    "description": values[0],
                    "message_to_send": f"{word} 可能指的是：{values[0]}"
                })
                return results
            else:
                results.append({
                    "title": f"{word} 可能是以下多个结果。",
                    "description": "选择此项以发送所有结果，或者选择下列选项以发送单项结果",
                    "message_to_send": f"{word} 可能指的是：" + "、".join(values)
                })
                for value in values:
                    results.append({
                        "title": value,
                        "description": "选择此项以发送该结果",
                        "message_to_send": f"{word} 可能指的是：{value}"
                    })
                return results
    else:
        results = []
        # full result

        result_before_removal = '，'.join(result['word'] for result in query_results)

        results.append({
            "title": f"查询结果中识别出了多个缩写组合：{result_before_removal}",
            "description": "选择此项以发送所有分词结果，或者选择下列选项以发送单词结果",
            "message_to_send": "\n".join(
                f"{result['word']} 可能指的是：" + "、".join(result["values"]) if result["values"] else
                    f"未找到 {result['word']} 指什么。如果您知道 {result['word']} 指什么，可以前往 https://lab.magiconch.com/nbnhhsh/ 提交结果。"
                for result in query_results
            )
        })

        for result in query_results:
            word = result["word"]
            result_type = result["type"]
            values = result["values"]

            if values:
                results.append({
                    "title": f"{word} 可能是以下结果：",
                    "description": "、".join(values),
                    "message_to_send": f"{word} 可能指的是：" + "、".join(values)
                })
            else:
                results.append({
                    "title": "找不到相关结果",
                    "description": f"您要是知道 {word} 指什么，可以前往 https://lab.magiconch.com/nbnhhsh/ 提交结果",
                    "message_to_send": f"未找到 {word} 指什么。如果您知道 {word} 指什么，可以前往 https://lab.magiconch.com/nbnhhsh/ 提交结果。"
                })
        return results

            


if __name__ == '__main__':
    word = input("word: ")
    result = query(word)
    print(stringify(result))