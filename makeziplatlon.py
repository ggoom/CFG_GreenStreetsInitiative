def try_cast(string):
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return string

    # print('"' in raw_lines[0].split(',')[0]) 
unwanted_indices = {1, 4, 5}

with open('data/zips.csv') as oldzips:
    raw_lines = oldzips.read().split('\n')[1:]
    new_lines = ['zip,lat,lon']
    for line in raw_lines:
        interm = [t.replace('"', '').replace(' ', '') for t in line.split(',')]
        final = [try_cast(x) for x in interm]
        want = [str(final[i]) for i in range(len(final)) if i not in unwanted_indices]
        new_lines.append(','.join(want))
    result_file_content = '\n'.join(new_lines)

    with open('data/ziplatlon.csv', 'w') as ziplatlon:
        ziplatlon.write(result_file_content)

