def triangle_judge(a: int, b: int, c: int) -> str:
    if a <= 0 or b <= 0 or c <= 0 or a > 200 or b > 200 or c > 200:
        return "边长数值越界"

    if a + b > c and a + c > b and b + c > a:
        if a == b == c:
            return "该三角形是等边三角形"
        if a == b or a == c or b == c:
            return "该三角形是等腰三角形"
        return "该三角形是普通三角形"

    return "所给三边数据不能构成三角形"







