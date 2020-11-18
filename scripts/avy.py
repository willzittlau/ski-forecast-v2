def get_avy_danger(avy_data):
    # Parse API data and create HTML strings to pass to Jinja
    danger_list = avy_data["dangerRatings"]
    date =[]
    # Write the 3 forecast days
    for danger_date in danger_list:
        string = '<h4>' + danger_date["date"][:10] + '</h4>'
        date.append(string)
    danger = []
    # Rename keys
    for dangers in danger_list:
        dangers['dangerRating']['Alpine'] = dangers['dangerRating'].pop('alp')
        dangers['dangerRating']['Treeline'] = dangers['dangerRating'].pop('tln')
        dangers['dangerRating']['Below Treeline'] = dangers['dangerRating'].pop('btl')
        danger.append(dangers['dangerRating'])
    return date, danger

def get_avy_problems(avy_data):
    # Create html string to pass to jinja from API data
    problems_list = []
    problems_data = avy_data["problems"]
    # Write problem type and expected size
    for problem in problems_data:
        output_string = '<h4><u>' + problem["type"] + '</u></h4>' + '<p><b>Expected Size = </b>'
        for key, value in problem["expectedSize"].items():
            output_string += key.title() + ': ' + value + ', '
        # Write Likelihood and Aspects
        output_string += '<b>Likelihood = </b>' + problem["likelihood"] + '</p><p><b>Aspects = </b>'
        for aspect in problem["aspects"]:
            output_string += aspect + ', '
        # Write elevations
        output_string += '<b>Elevations = </b>'
        for elevation in problem["elevations"]:
            elevation = convert_elevtxt(elevation)
            output_string += elevation + ', '
        # Clean up final output string
        output_string = output_string[:-2]
        output_string += '</p><p>' + problem["comment"] + '</p>'
        problems_list.append(output_string)
    return problems_list

def get_avy_summary(avy_data):
        summary = []
        summary.append("<h3>Highlights:</h3>" + avy_data["highlights"])
        summary.append("<h3>Avalanche Summary:</h3>" + avy_data["avalancheSummary"])
        summary.append("<h3>Snowpack Summary:</h3>" + avy_data["snowpackSummary"])
        summary.append("<h3>Regional Summary:</h3>" + avy_data["weatherForecast"])
        return summary