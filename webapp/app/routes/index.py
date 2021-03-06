from app import app
from app import APP_STATIC
import os
import json
from flask.ext.restful.reqparse import RequestParser
from flask import jsonify
from context import campaignadvisor

map_data_name = campaignadvisor.dataframe_holder.MAP_DATA
map_data = campaignadvisor.dataframe_holder.get_dataframe(map_data_name)
@app.route('/')

def root():
	return app.send_static_file('index.html')

@app.route('/api/getCountyStatisticsColumns', methods=['GET'])
def get_county_statistics_column():
	return jsonify(data_points=list(map_data.columns)), 200

@app.route('/api/getCountyLines', methods=['GET'])
def get_county_lines():
	return app.send_static_file('mapdata/county.json')
	
@app.route('/api/getStateLines', methods=['GET'])
def get_state_lines():
	return app.send_static_file('mapdata/states.json')

@app.route('/api/getCountyStatistics', methods=['POST'])
def get_county_statistics():
	parser = RequestParser()
	parser.add_argument('data_column', required=True, type=str, location='json',
						help='Data column is needed.')
	args = parser.parse_args()
	try:
		series_needed = map_data[args.data_column]
		max_value = series_needed.max()
		min_value = series_needed.min()
		json_doc = json.loads(series_needed.to_json())
		return jsonify(county_data=json_doc,
						max_value=max_value,
						min_value=min_value)
	except:
		return 'Column does not exist'
    # Unreachable code
	#return 'success', 200


