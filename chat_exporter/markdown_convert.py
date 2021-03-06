import re


async def parse_markdown(content):
    # **bold**
    pattern = re.compile(r"\*\*(.*?)\*\*")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '<strong>%s</strong>' % affected_text)
        match = re.search(pattern, content)

    # *italic*
    pattern = re.compile(r"\*(.*?)\*")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '<em>%s</em>' % affected_text)
        match = re.search(pattern, content)

    # __underline__
    pattern = re.compile(r"__(.*?)__")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '<span style="text-decoration: underline">%s</span>' % affected_text)
        match = re.search(pattern, content)

    # ~~strikethrough~~
    pattern = re.compile(r"~~(.*?)~~")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '<span style="text-decoration: line-through">%s</span>' % affected_text)
        match = re.search(pattern, content)

    # ||spoiler||
    pattern = re.compile(r"\|\|(.*?)\|\|")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '<span class="spoiler spoiler--hidden" onclick="showSpoiler(event, this)">'
                                  '<span class="spoiler-text">%s</span></span>' % affected_text)
        match = re.search(pattern, content)

    # > quote
    pattern = re.compile(r"^&gt;\s(.+)")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        br_pattern = re.compile(r"^&gt;\s(.+?)<br>")
        if re.search(br_pattern, content):
            match = re.search(br_pattern, content)
            affected_text = match.group(1)
            content = content.replace(content[match.start():match.end()],
                                      '<div class="quote">%s</div>' % affected_text)
        else:
            content = content.replace(content[match.start():match.end()],
                                      '<div class="quote">%s</div>' % affected_text)
        match = re.search(pattern, content)

    pattern = re.compile(r"<br>&gt;\s(.+)")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        br_pattern = re.compile(r"<br>&gt;\s(.+?)<br>")
        if re.search(br_pattern, content):
            match = re.search(br_pattern, content)
            affected_text = match.group(1)
            content = content.replace(content[match.start():match.end()],
                                      '<div class="quote">%s</div>' % affected_text)
        else:
            content = content.replace(content[match.start():match.end()],
                                      '<div class="quote">%s</div>' % affected_text)
        match = re.search(pattern, content)

    # ```code```
    pattern = re.compile(r"```(.*?)```")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        affected_text = re.sub(r"^<br>", "", affected_text)
        affected_text = re.sub(r"<br>$", "", affected_text)
        affected_text = await return_to_markdown(affected_text)
        content = content.replace(content[match.start():match.end()],
                                  '<div class="pre pre--multiline nohighlight">%s</div>' % affected_text)
        match = re.search(pattern, content)

    # ``code``
    pattern = re.compile(r"``(.*?)``")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        affected_text = await return_to_markdown(affected_text)
        content = content.replace(content[match.start():match.end()],
                                  '<span class="pre pre-inline">%s</span>' % affected_text)
        match = re.search(pattern, content)

    # `code`
    pattern = re.compile(r"`(.*?)`")
    match = re.search(pattern, content)
    while match is not None:
        affected_text = match.group(1)
        affected_text = await return_to_markdown(affected_text)
        content = content.replace(content[match.start():match.end()],
                                  '<span class="pre pre-inline">%s</span>' % affected_text)
        match = re.search(pattern, content)

    return content


spoiler = r''


async def return_to_markdown(content):
    # content = re.sub(r"^<br>", "", content)

    for match in re.finditer(r"<strong>(.*?)</strong>", content):
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '**%s**' % affected_text)

    for match in re.finditer(r"<em>([^<>]+)</em>", content):
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '*%s*' % affected_text)

    for match in re.finditer(r'<span style="text-decoration: underline">([^<>]+)</span>', content):
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '__%s__' % affected_text)

    for match in re.finditer(r'<span style="text-decoration: line-through">([^<>]+)</span>', content):
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '~~%s~~' % affected_text)

    for match in re.finditer(r'<span class="spoiler spoiler--hidden" onclick="showSpoiler\(event, this\)">'
                             r'<span class="spoiler-text">(.*?)</span></span>', content):
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '||%s||' % affected_text)

    for match in re.finditer(r'<div class="quote">(.*?)</div>', content):
        affected_text = match.group(1)
        content = content.replace(content[match.start():match.end()],
                                  '> %s' % affected_text)

    return content
