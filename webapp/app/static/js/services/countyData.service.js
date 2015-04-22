angular.module('CampaignAdvisor')
  .factory('countyDataService', ['$resource', function ($resource) {
  	var countyDataService = {};
  	var countyStatisticsResource = $resource('/api/getCountyStatistics', {}, {
      getCountyStatistics: {
        method: 'POST'
      }, 
      getCountyStatisticsColumns: {
      	method: 'GET',
      	url: '/api/getCountyStatisticsColumns'
      }
    });
    var PERCENTAGE_DATA = ['percent', 'Pct', 'pct', 'percentage'];
  	countyDataService.getData = function(columnName) {
  		return countyStatisticsResource.getCountyStatistics({ data_column: columnName}).$promise.then(function (countyData) {
  			return countyDataService.normalizeData(columnName, countyData);
  		});
  	};
  	countyDataService.normalizeData = function(columnName, countyData) {
  		var min = countyData.min_value;
  		var max = countyData.max_value;
  		countyData = countyData.county_data;
      console.log(countyData);
  		var isPct = PERCENTAGE_DATA.some(function(str) {
        return columnName.indexOf(str) != -1;
      });
  		var dataArray = Object.keys(countyData).map(function(countyDataKey) {
  			var dataPoint = [];
  			dataPoint[0] = countyDataKey;
  			dataPoint[1] = countyData[countyDataKey];
  			return dataPoint;
  		});

  		if (isPct) {
  			return { countyData: transformToObj(dataArray), min: min, max: max} ;
  		} else {
  			var range = max - min;
  			dataArray = dataArray.map(function(d) {
  				d[1] = (d[1] - min) / range * 100;
  				return d;
  			});
        console.log(dataArray);
  			return { countyData: transformToObj(dataArray), min: min, max: max} ;
  		}
  	};

  	countyDataService.getCountyStatisticsColumns = function() {
  		return countyStatisticsResource.getCountyStatisticsColumns().$promise;
  	}

  	function transformToObj(normalizedData) {
  		return normalizedData.reduce(function(accum, data) {
  			accum[data[0]] = data[1];
  			return accum;
  		}, {});
  	}
    return countyDataService;
  }]);
