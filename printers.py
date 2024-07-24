
def format_as_json(data, indent=4):
    def format_value(value, indent, level):
        if isinstance(value, dict):
            return format_dict(value, indent, level)
        elif isinstance(value, list):
            return format_list(value, indent, level)
        elif isinstance(value, tuple):
            return format_tuple(value, indent, level)
        elif isinstance(value, set):
            return format_set(value, indent, level)
        elif isinstance(value, str):
            return f'"{value}"'
        else:
            return str(value)

    def is_primitive(value):
        return not isinstance(value, (dict, list, tuple, set))

    def format_dict(d, indent, level):
        if all(is_primitive(v) for v in d.values()) and len(d) <= 3:
            items = [f'"{k}": {format_value(v, indent, level)}' for k, v in d.items()]
            return "{" + ", ".join(items) + "}"
        items = [f'{" " * (level + indent)}"{k}": {format_value(v, indent, level + indent)}' for k, v in d.items()]
        return "{\n" + ",\n".join(items) + "\n" + " " * level + "}"

    def format_list(l, indent, level):
        if all(is_primitive(item) for item in l):
            items = [format_value(item, indent, level) for item in l]
            return "[" + ", ".join(items) + "]"
        items = [f'{" " * (level + indent)}{format_value(item, indent, level + indent)}' for item in l]
        return "[\n" + ",\n".join(items) + "\n" + " " * level + "]"

    def format_tuple(t, indent, level):
        if all(is_primitive(item) for item in t):
            items = [format_value(item, indent, level) for item in t]
            return "(" + ", ".join(items) + ")"
        items = [f'{" " * (level + indent)}{format_value(item, indent, level + indent)}' for item in t]
        return "(\n" + ",\n".join(items) + "\n" + " " * level + ")"

    def format_set(s, indent, level):
        if all(is_primitive(item) for item in s):
            items = [format_value(item, indent, level) for item in s]
            return "{" + ", ".join(items) + "}"
        items = [f'{" " * (level + indent)}{format_value(item, indent, level + indent)}' for item in s]
        return "{\n" + ",\n".join(items) + "\n" + " " * level + "}"

    return format_value(data, indent, 0)

if __name__ == "__main__":
    data = {
        "name": "John",
        "age": 30,
        "children": [
            ("Anna", 10),
            ("Ben", 12)
        ],
        "animal": (
            ["frog", 2],
            ["dog", 5]
        ),
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "Teste": "Hello"
        },
        "skills": {"Python", "Java", "C++"}
    }

    
    print("ISSO AQUI É COMPLETAMENTE DESNECESSÁRIO!!")
    print(format_as_json(data))
