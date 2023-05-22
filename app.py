from flask import Flask, render_template, request
from wtforms import Form, StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired
import os
import openai

app = Flask(__name__)


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
        property_type = request.form['property_type']
        location = request.form['location']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        en_suite_bathrooms = request.form['en_suite_bathrooms']
        square_footage = request.form['square_footage']
        community = request.form['community']
        driveway = request.form['driveway']
        garage = request.form['garage']
        outdoor_features = request.form['outdoor_features']
        additional_exterior = request.form['additional_exterior']
        special_rooms = request.form['special_rooms']
        flooring_type = request.form['flooring_type']
        special_features = request.form['special_features']
        natural_light = request.form['natural_light']
        decorative_style = request.form['decorative_style']
        kitchen_layout = request.form['kitchen_layout']
        kitchen_fittings = request.form['kitchen_fittings']
        kitchen_features = request.form['kitchen_features']
        bathroom_details = request.form['bathroom_details']
        security_features = request.form['security_features']
        character_details = request.form['character_details']
        points_of_interest = request.form['points_of_interest']
        recent_updates = request.form['recent_updates']

        openai.api_key = os.getenv("OPENAI_API_KEY")
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

        messages = [
            {"role": "system", "content": "You are an estate agent salesperson, Your job is to write a beautiful description of a property based on data given to you about a property. The description should be detailed and should use the best sales tactics to really sell the property"},
            {"role": "user", "content": f"Let's think about this step-by-step. {prompt}"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )
        description = response["choices"][0]["message"]["content"]
        print(description)
        return render_template('result.html', description=description)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
