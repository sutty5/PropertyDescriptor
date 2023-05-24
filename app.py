from flask import Flask, render_template, request, Response, session, flash
from wtforms import Form, StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired
import os
import openai
import base64
import secrets
import string


app = Flask(__name__)
app.secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))


class InputForm(Form):
    property_type = StringField('Property Type', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    bedrooms = IntegerField('Number of Bedrooms', validators=[DataRequired()])
    bathrooms = IntegerField('Number of Bathrooms', validators=[DataRequired()])
    en_suite_bathrooms = IntegerField('Number of En Suite Bathrooms')
    square_footage = IntegerField('Square Footage', validators=[DataRequired()])
    community = StringField('Community or Complex')
    driveway = StringField('Driveway Type')
    garage = StringField('Garage Details')
    outdoor_features = StringField('Outdoor Features')
    additional_exterior = StringField('Additional Exterior Details')
    special_rooms = StringField('Special Rooms or Features')
    flooring_type = StringField('Flooring Type')
    special_features = StringField('Special Features')
    natural_light = StringField('Natural Light and Views')
    decorative_style = StringField('Decorative Style')
    kitchen_layout = StringField('Kitchen Layout')
    kitchen_fittings = StringField('Kitchen Fittings')
    kitchen_features = StringField('Special Kitchen Features')
    bathroom_details = StringField('Bathroom Details')
    security_features = StringField('Security Features')
    character_details = StringField('Character or Historic Details')
    points_of_interest = StringField('Nearby Points of Interest')
    recent_updates = StringField('Recent Updates or Renovations')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():

        prompt = f"Write a description for a {form.property_type.data} located in {form.location.data} with {form.bedrooms.data} bedrooms, {form.bathrooms.data} bathrooms, {form.square_footage.data} square feet."
        # Add details that might not be applicable for every property
        if form.community.data:
            prompt += f" The property is part of a community or complex named {form.community.data}."
        if form.driveway.data:
            prompt += f" The exterior of the property features a {form.driveway.data} driveway."
        if form.garage.data:
            prompt += f" It has a {form.garage.data}."
        if form.outdoor_features.data:
            prompt += f" Outdoor features include {form.outdoor_features.data}."
        if form.additional_exterior.data:
            prompt += f" Additional exterior details include {form.additional_exterior.data}."
        if form.special_rooms.data:
            prompt += f" Inside, the property boasts special rooms such as {form.special_rooms.data}."
        if form.flooring_type.data:
            prompt += f" The property has {form.flooring_type.data} flooring."
        if form.special_features.data:
            prompt += f" Special features of the property include {form.special_features.data}."
        if form.natural_light.data:
            prompt += f" The property benefits from {form.natural_light.data}."
        if form.decorative_style.data:
            prompt += f" The property is decorated in a {form.decorative_style.data} style."
        if form.kitchen_layout.data:
            prompt += f" The kitchen is {form.kitchen_layout.data}."
        if form.kitchen_fittings.data:
            prompt += f" It is fitted with {form.kitchen_fittings.data}."
        if form.kitchen_features.data:
            prompt += f" Special kitchen features include {form.kitchen_features.data}."
        if form.bathroom_details.data:
            prompt += f" The bathrooms feature {form.bathroom_details.data}."
        if form.en_suite_bathrooms.data:
            prompt += f" The property has {form.en_suite_bathrooms.data} en suite bathrooms."
        if form.security_features.data:
            prompt += f" Security features of the property include {form.security_features.data}."
        if form.character_details.data:
            prompt += f" The property boasts {form.character_details.data}."
        if form.points_of_interest.data:
            prompt += f" Nearby points of interest include {form.points_of_interest.data}."
        if form.recent_updates.data:
            prompt += f" Recent updates or renovations include {form.recent_updates.data}."

        session['prompt'] = prompt
        return render_template('result.html')
    return render_template('index.html', form=form)


@app.route('/stream')
def stream():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = [
        {"role": "system",
         "content": "You are a world renowned estate agent salesperson, Your job is to write a beautiful description of a property based on data given to you about a property. The description should be detailed, and should use the best sales tactics to really sell the property. Highlight the unique selling points, Create an emotional connection, Use persuasive language, Keep it concise and easy to read, but most importantly keep it realistic and accurate."},
        {"role": "user", "content": session['prompt']}
        # Get the prompt from the session
    ]

    def generate_response():
        retry_limit = 5
        for attempt in range(retry_limit):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    stream=True
                )
                collected_messages = ""
                for chunk in response:
                    if "content" in chunk["choices"][0]["delta"]:
                        message_chunk = chunk["choices"][0]["delta"]["content"]
                        collected_messages += message_chunk
                        encoded_message = base64.b64encode(collected_messages.strip().encode()).decode()
                        yield f"data: {encoded_message}\n\n"
                messages.append({"role": "assistant", "content": collected_messages})
                print(collected_messages)
                yield 'event: end\ndata: close\n\n'  # Add this line
                break  # If successful, break out of the loop
            except Exception as e:
                print(f"Error encountered during OpenAI request: {e}")
                if attempt + 1 == retry_limit:
                    print("Reached maximum retry limit. Aborting.")
                    yield 'event: end\ndata: error\n\n'  # Send error signal to the client
                    break
                print("Retrying...")

    return Response(generate_response(), content_type="text/event-stream")


if __name__ == '__main__':
    app.run(host='192.168.86.39', port=5000)