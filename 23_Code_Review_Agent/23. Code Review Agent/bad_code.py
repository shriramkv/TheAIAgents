def calculate_total(items):
    total = 0
    for i in range(len(items)):
        total += items[i]
    return total

def process_data(data):
    # This function does too much
    result = []
    for d in data:
        if d > 10:
            result.append(d * 2)
        else:
            result.append(d + 5)
            
    # Save to file (side effect)
    f = open('output.txt', 'w')
    f.write(str(result))
    f.close()
    
    return result
