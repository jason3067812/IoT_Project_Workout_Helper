from flask import Flask
from pymongo import MongoClient
from flask import request, render_template


app = Flask(__name__, template_folder="templates/", static_folder="")

uri = "mongodb+srv://eric:qwert1234@cluster0.xweafpe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.iot_final
sensor = db.sensor_data
userInput = db.userInput

def find_exist(filtered_reps, rep):
    for i in filtered_reps:
        if i[0]==rep['date'] and i[1]==rep['type']:
            i[2] += 1
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    reps = sensor.find({"date" : { '$exists' : True } })
    sets = sensor.find({"date_s" : { '$exists' : True } })
    b_count = sensor.count_documents({"type":"bench press"})
    s_count = sensor.count_documents({"type":"squat"})
    if request.method == 'POST':
        if request.form.get('submit'):
            start = request.form.get('start')
            start_original = start
            start = start.replace('-','')
            end = request.form.get('end')
            end_original = end
            end = end.replace('-','')
            filter = request.form.get('Exercise')
            filtered_reps = list()
            dates = []
            exercises = []
            numberReps = []
            numberSets = []
            repsPerSet = []
            numberB = 0
            numberS = 0

            for rep in reps:
                if int(rep['date'].replace('-','')) <= int(end) and int(rep['date'].replace('-',''))  \
                >= int(start):
                    if rep['type']=='bench press':
                        numberB += 1
                    elif rep['type']=='squat':
                        numberS += 1
                    if rep['type']==filter:
                        if find_exist(filtered_reps,rep):
                            pass
                        else:
                            date_exercise = [rep['date'],rep['type'],1]
                            filtered_reps.append(date_exercise)                     
                    
            filtered_reps = sorted(filtered_reps)

            for filtered_rep in filtered_reps:
                set_count = 0
                print(filtered_rep[0])
                for set in sets:
                    print(set['date_s'])
                    print(set['type_s'])
                    if set['date_s']==filtered_rep[0] and set['type_s']==filtered_rep[1]:
                        set_count += 1
                sets.rewind()
                dates.append(filtered_rep[0])
                exercises.append(filtered_rep[1])
                numberReps.append(filtered_rep[2])
                numberSets.append(set_count)
                repsPerSet.append(int(filtered_rep[2]/set_count) if set_count > 0 else filtered_rep[2])

            print(numberSets)

            return render_template("index.html",dates=dates,exercises=exercises,
            numberReps=numberReps,numberSets=numberSets,repsPerSet=repsPerSet,filter=filter,start=start_original,end=end_original,numberB=numberB,
            numberS=numberS)

    return render_template("index.html",b_count=b_count,s_count=s_count)


@app.route('/input', methods=['GET', 'POST'])
def input():
    userInfoQuery = {}
    userInfo = userInput.find_one(userInfoQuery)
    height = userInfo['height']
    lengthofarm  = userInfo['lengthofarm']
    lengthofleg = userInfo['lengthofleg']

    if request.method == 'POST':
        if request.form.get('submit'):
            userInput.delete_many({})
            height = request.form.get('height')
            lengthofarm = request.form.get('lengthofarm')
            lengthofleg = request.form.get('lengthofleg')
            input  = { "height": height, "lengthofarm": lengthofarm, "lengthofleg":lengthofleg}
            x = userInput.insert_one(input)

    return render_template("input.html",height=height,lengthofarm=lengthofarm,lengthofleg=lengthofleg)


if __name__ == "__main__":
  import click
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True, threaded=threaded)

  run()