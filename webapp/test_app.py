import pytest
from unittest.mock import Mock, patch

from app import app


@pytest.fixture
def client():
	app.config["TESTING"] = True
	with app.test_client() as test_client:
		yield test_client


def test_index(client):
	with patch("app.render_template", return_value="index") as render:
		response = client.get("/")

	assert response.status_code == 200
	assert response.get_data(as_text=True) == "index"
	render.assert_called_once_with("index.html")


@pytest.mark.parametrize(
	("model_result", "expected_prediction"),
	[
		(0, "Iris-Setosa"),
		(1, "Iris-Versicolor"),
		(2, "Iris-Virginica"),
	],
)
def test_predict(client, model_result, expected_prediction):
	model = Mock()
	model.predict.return_value = model_result

	form_data = {
		"sepal_length": "5.1",
		"sepal_width": "3.5",
		"petal_length": "1.4",
		"petal_width": "0.2",
	}

	with patch("app.open", create=True), patch(
		"app.pickle.load", return_value=model
	), patch("app.requests.post") as post, patch(
		"app.render_template", return_value="prediction"
	) as render:
		response = client.post("/predict", data=form_data)

	assert response.status_code == 200
	assert response.get_data(as_text=True) == "prediction"
	model.predict.assert_called_once_with([[5.1, 3.5, 1.4, 0.2]])
	post.assert_called_once_with(
		url="http://p5dbapp:8001/add_records",
		json={
			"sepal_length": 5.1,
			"sepal_width": 3.5,
			"petal_length": 1.4,
			"petal_width": 0.2,
			"prediction": expected_prediction,
		},
	)
	render.assert_called_once_with("predict.html", prediction=expected_prediction)



def test_records(client):
	records = [{"prediction": "Iris-Setosa"}]
	database_response = Mock()
	database_response.json.return_value = records

	with patch("app.requests.get", return_value=database_response) as get, patch(
		"app.render_template", return_value="records"
	) as render:
		response = client.get("/records")

	assert response.status_code == 200
	assert response.get_data(as_text=True) == "records"
	get.assert_called_once_with("http://p5dbapp:8001/records")
	render.assert_called_once_with("records.html", records=records)
