from django.shortcuts import render
import random

def home(request):
    if 'secret' not in request.session:
        digits = random.sample("123456789", 4)
        num = int("".join(digits))
        tom = []
        jerry = []
        exp = 1
        ram = num
        while ram != 0:
            tom.append(ram % 10)
            jerry.append((ram % 10) * exp)
            exp *= 10
            ram = ram // 10

        request.session['secret'] = num
        request.session['tom'] = tom
        request.session['jerry'] = jerry
        request.session['score'] = 0
        request.session['history'] = []

    message = ""
    won = False

    if request.method == 'POST':
        user_input = request.POST.get('guess', '')

        if len(user_input) == 4 and user_input.isdigit() and '0' not in user_input:
            
            # Check for repeating digits
            u = []
            m = int(user_input)
            temp = m
            while temp != 0:
                if temp % 10 not in u:
                    u.append(temp % 10)
                temp = temp // 10

            if len(u) == 4:
                request.session['score'] += 1
                score = request.session['score']

                user = int(user_input)
                num = request.session['secret']

                if user == num:
                    message = f"🎉 You guessed it in {score} attempts!"
                    won = True
                    history = request.session['history']
                    history.append({
                        "guess": user_input,
                        "correct_digits": 4,
                        "correct_position": 4
                    })
                    request.session['history'] = history
                    request.session.flush()
                else:
                    # YOUR exact logic for counting!
                    tom = request.session['tom']
                    jerry = request.session['jerry']
                    count = 0
                    coun = 0
                    exp = 1
                    temp = user
                    while temp != 0:
                        if temp % 10 in tom:
                            count += 1
                        if (temp % 10) * exp in jerry:
                            coun += 1
                        temp = temp // 10
                        exp *= 10

                    message = f"🔢 {count} digits correct, {coun} in right position!"

                    history = request.session['history']
                    history.append({
                        "guess": user_input,
                        "correct_digits": count,
                        "correct_position": coun
                    })
                    request.session['history'] = history
                    request.session.modified = True
            else:
                message = "⚠️ Enter 4 unique digits without repetition!"
        else:
            message = "⚠️ Enter a valid 4 digit number without zero!"

    return render(request, 'game/home.html', {
        'message': message,
        'score': request.session.get('score', 0),
        'history': request.session.get('history', []),
        'won': won
    })
 