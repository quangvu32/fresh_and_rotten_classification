# Project Structure

```
project/
│
├── app.py                # Flask application (backend)
├── static/
│   ├── styles.css
    ├── uploads/
    ├── model2.h5
├── templates/
│   ├── index.html        # HTML template

```

Dataset link: https://www.kaggle.com/datasets/swoyam2609/fresh-and-stale-classification



Tutorial:

  Install necessary library: pip install flask gdown numpy tensorflow werkzeug pillow
  
  To lunch: python app.py

  By default it will run on: http://127.0.0.1:5000/. But you can modify it by looking for this block of code at the end of app.py
```
  if __name__ == '__main__':
    app.run(debug=True)
```

  You can modify it into like this:
  
```
  if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

 This would launch the app on http://0.0.0.0:8080/ . You can modify it if you want
