
import pandas as pd
import re
from transformers import pipeline

dataset = pd.read_csv(r"C:\Users\CHIRNAJIV ZOPE\Downloads\real_cutoff_dataset.csv")
dataset.head()

generator=pipeline("text-generation",model='TinyLlama/TinyLlama-1.1B-Chat-v1.0')

def college_recomender(percentile,branch,location):
  filtered=dataset[

    (dataset['branch'].str.contains(branch , case=False , na=False)) &
    (dataset['location'].str.contains(location , case=False , na=False)) &
    (dataset['percentile']<=percentile )]
  return filtered.sort_values(by="percentile",ascending=False)


def classify_colleges(result,user_percentile):
  dream=result[result['percentile']>user_percentile+2]
  target=result[(result['percentile']<=user_percentile) &
                (result['percentile']>user_percentile-2)]
  safe=result[result['percentile']<=user_percentile-2]
  return dream,target,safe
def format_df(df):
  if df.empty:
    return 'None'
  else:
    return "\n".join(
        [f"- {row['college']}({row['percentile']})"
        for _ , row in df.head(3).iterrows()]
        )


def handle_query(query: str):
  try:
    if "," in query:
        parts=query.split(",")
        percentile=float(parts[0].strip())
        branch=parts[1].strip().title()
        location=parts[2].strip().title()

        loc=[
        'Amravati',
        'Aurangabad',
        'Kolhapur',
        'Mumbai',
        'Nagpur',
        'Nashik',
        'Pune',
        'Sangli'
        ]

        branches = [
        'Civil Engineering',
        'Computer Engineering',
        'Electrical Engineering',
        'Electronics Engineering',
        'IT',
        'Mechanical Engineering'
          ]
        if branch not in branches:
          return f""" Invalid branch. choose from {branches}"""
        if location not in loc:
          return f""" Invalid location. choose from {loc} """
    
        

        result=college_recomender(percentile,branch,location)
        dream,target,safe=classify_colleges(result,percentile)
        return f""" According to your percentile-{percentile} and your location-{location}
        and branch-{branch} your colleges according to your dream are
        Dream-{format_df(dream)}
        Target-{format_df(target)}
        Safe-{format_df(safe)}
        """
    elif "percentile" in query.lower():
        percentile_match=re.search(r'\d+\.?\d*',query)
        percentile=float(percentile_match.group()) if percentile_match else None
        loc=[
        'Amravati',
        'Aurangabad',
        'Kolhapur',
        'Mumbai',
        'Nagpur',
        'Nashik',
        'Pune',
        'Sangli'
        ]
        branches = [
        'Civil Engineering',
        'Computer Engineering',
        'Electrical Engineering',
        'Electronics Engineering',
        'IT',
        'Mechanical Engineering'
        ]
        location=None
        for l in loc:
          if l.lower() in query.lower():
           location=l
          
        branch=None
        for b in branches:
          if b.lower() in query.lower():
           branch=b
        if percentile is None or branch is None or location is None:
         return "⚠️ Please provide percentile, branch, and location clearly."
        result=college_recomender(percentile,branch,location)
        dream,target,safe=classify_colleges(result,percentile)
        return f""" According to your percentile-{percentile} and your preferred city-{location}
        and branch-{branch} your colleges according to your dream are
        Dream-{format_df(dream)}
        Target-{format_df(target)}
        Safe-{format_df(safe)}
        """


    else:
       response=generator(f"<|user|>\n{query.strip()}\n<|assistant|>\n",temperature=0.7,do_sample=True,max_new_tokens=50)
       ans=response[0]["generated_text"]
       text=ans.split("<|assistant|>")[-1].strip() 
       if "<|user|>" in text:
         return text.replace("<|user|>","").strip()
       return text

  except Exception as e:
    return f" Error: {str(e)}\nPlease enter in format: percentile,branch,location"


# while True:
#   user_input = input("you:")
#   if user_input=="exit":
#     break
#   else:
#     print('bot :',handle_query(user_input))