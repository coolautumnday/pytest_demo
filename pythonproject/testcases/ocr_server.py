from flask import Flask, request, jsonify
from rapidocr import RapidOCR
import cv2
import os

app = Flask(__name__)

# 全局加载模型，只初始化一次
ocr_engine = RapidOCR(params={
    "Det.box_thresh": 0.45,
    "Det.unclip_ratio": 1.8,
    "Det.limit_side_len": 2000,
})

@app.route("/ocr", methods=["POST"])
def ocr_api():
    """
    请求JSON入参：{"img_path": "D:\\test\\app_screen.png"}
    返回：[{"text": "文字", "box": [[x1,y1],[x2,y2],[x3,y3],[x4,y4]], "score": 置信度}]
    box：原图四点像素坐标
    """
    try:
        json_data = request.get_json()
        img_path = json_data.get("img_path")
        if not img_path:
            return jsonify({"code": 400, "msg": "缺少参数 img_path（图片绝对路径）"}), 400

        # 判断文件是否存在
        if not os.path.exists(img_path):
            return jsonify({"code": 400, "msg": f"文件不存在：{img_path}"}), 400

        img = cv2.imread(img_path)
        if img is None:
            return jsonify({"code": 400, "msg": "图片读取失败，请检查路径"}), 400

        # return_word_box=False：整行框；True：单字框
        result = ocr_engine(img, return_word_box=False)
        res_list = []
        for box, text, score in zip(result.boxes, result.txts, result.scores):
            res_list.append({
                "text": text,
                "box": box.tolist(),
                "score": round(float(score), 3)
            })

        # 可选：开启同行文字合并，取消下面这行注释
        # res_list = merge_same_line(res_list)

        return jsonify({
            "code": 200,
            "data": res_list
        })
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务异常: {str(e)}"}), 500


# 可选：合并同一行文字的函数
def merge_same_line(ocr_result, y_threshold=12):
    def get_center_y(item):
        ys = [p[1] for p in item["box"]]
        return sum(ys)/len(ys)
    ocr_result.sort(key=get_center_y)
    lines = []
    for item in ocr_result:
        cy = get_center_y(item)
        find_line = False
        for line in lines:
            line_cy = get_center_y(line[0])
            if abs(cy - line_cy) < y_threshold:
                line.append(item)
                find_line = True
                break
        if not find_line:
            lines.append([item])
    merged = []
    for line in lines:
        line.sort(key=lambda x: x["box"][0][0])
        all_text = "".join([i["text"] for i in line])
        all_boxes = [p for i in line for p in i["box"]]
        xs = [p[0] for p in all_boxes]
        ys = [p[1] for p in all_boxes]
        new_box = [min(xs),min(ys),max(xs),max(ys)] # #左上右下
        avg_score = round(sum([i["score"] for i in line])/len(line),3)
        merged.append({"text":all_text,"box":new_box,"score":avg_score})
    return merged


if __name__ == '__main__':
    # 单进程启动，禁止多进程
    app.run(host="0.0.0.0", port=9003, processes=1, debug=False)
