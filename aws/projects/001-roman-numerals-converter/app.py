from flask import Flask, render_template, request

converter_app = Flask(__name__)

@converter_app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == 'POST':    
        user_input = request.form["number"]
        if user_input.isalpha() or user_input == "0":
            return render_template("index.html", developer_name = "E2227", not_valid= True)
        else:
            user_input = int(user_input)
        if user_input >= 4000 or user_input < 1 :
            return render_template("index.html", developer_name = "E2227", not_valid= True)
        else:
            val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
            syb = ["M", "CM", "D", "CD","C", "XC", "L", "XL","X", "IX", "V", "IV", "I"]
            number_roman = ''
            number_decimal = user_input
            i = 0
            while  user_input > 0:
	            for j in range(user_input // val[i]):
	                number_roman += syb[i]
	                user_input -= val[i]
	            i += 1
            return render_template("result.html", developer_name = "E2227", number_decimal = number_decimal, number_roman=number_roman)
    else:
        return render_template("index.html", developer_name = "E2227")
        

if __name__ == '__main__':
    #converter_app.run(debug = True)
    converter_app.run(host='0.0.0.0', port=80)