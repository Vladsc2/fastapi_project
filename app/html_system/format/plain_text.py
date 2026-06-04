
async def format_all_lines(text: str) -> str:
    lines = text.split("\n")

    lines = _clear_empty_start_lines(lines)

    lines = _strip_all_lines( lines )

    text = _glue_lines( lines )

    return text


def _clear_empty_start_lines(lines: list[str]) -> list[str]:
    new_lines = []
    is_start = True
    for line in lines:
        if is_start and line == "":
            continue
        else:
            is_start = False
            new_lines.append( line )

    return new_lines


def _find_min_space_index(lines: list[str]) -> int:
    min_index = 99999
    for line in lines:
        if line.strip() == "":
            continue

        index = 0

        for char in line:
            if char == " ":
                index += 1
            else:
                break

        if index < min_index:
            min_index = index

    if min_index == 99999:
        min_index = 0
    return min_index


def _strip_all_lines(lines: list[str]) -> list[str]:
    min_index = _find_min_space_index(lines)

    formated_lines = []
    for line in lines:
        line = line[min_index:].rstrip()
        formated_lines.append( line )

    return formated_lines


def _glue_lines(lines: list[str]) -> str:
    text = ""
    for line in lines:
        text += line + "\n"
    return text
