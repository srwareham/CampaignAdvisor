angular.module('CampaignAdvisor')
  .controller('HomeController', ['$scope', 'countyLines', 'stateLines', 'drawMap', '$timeout', '$q', 'countyDataService', '$location',
  	function ($scope, countyLines, stateLines, drawMap, $timeout, $q, countyDataService, $location) {
  	drawMap.setGeojson(stateLines, countyLines);
    drawMap.drawStates(1);
    drawMap.drawStates(2);

    var stateFips = ["10", "11", "12", "13", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56", "01", "02", "04", "05", "06", "08", "09"];
    $scope.nextPage = function(next) {
      $location.url(next);
    };
    $scope.mapState = {
      1: {
        state: false
      },
      2: {
        state: false
      }
    };
	     

    $scope.zoomToState = function(state) {
      drawMap.zoomToState(state.value);
    }

    $scope.mapZoomOut = function(mapNumber) {
      drawMap.reset(mapNumber);
    };
    /**
     * Build `states` list of key/value pairs
     */
    function loadAll() {
      var allStates = 'Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware,\
              Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana,\
              Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana,\
              Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina,\
              North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina,\
              South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia,\
              Wisconsin, Wyoming';
      return allStates.split(/, +/g).map( function (state) {
        return {
          value: state.toLowerCase(),
          display: state
        };
      });
    }
    /**
     * Create filter function for a query string
     */
    function createFilterFor(query) {
      var lowercaseQuery = angular.lowercase(query);
      return function filterFn(state) {
        return (state.value.indexOf(lowercaseQuery) === 0);
      };
    }
    $scope.drawAllCounties = function(mapNumber, state) {
      if (state) {
        drawMap.drawAllCounties(mapNumber);
        $scope.mapState[mapNumber].state = state;
      } else {
        console.log('removing');
        drawMap.removeAllCounties(mapNumber);
        $scope.mapState[mapNumber].state = state;
      }
    }
   // $scope.drawAllCounties(1);
   // $scope.drawAllCounties(2);
   // 
   $scope.$watch('mapState[1].state', function() {
    if ($scope.mapState[1].state) {
      $scope.drawAllCounties(1, true);
    } else {
      $scope.drawAllCounties(1, false);
    }
   });

   $scope.$watch('mapState[2].state', function() {
    if ($scope.mapState[2].state) {
      if ($scope.mapState[2].state) {
        $scope.drawAllCounties(2, true);
      } else {
        $scope.drawAllCounties(2, false);
      }
    }
   });

    $scope.loadDataPoints = function() {
    // Use timeout to simulate a 650ms request.
      $scope.dataPoints = []
      return $timeout(function() {
        countyDataService.getCountyStatisticsColumns().then(function(res) {
          $scope.dataPoints = res.data_points;
        });
      }, 1000);
    };

    $scope.$watch('dataPoint', function() {
      if ($scope.dataPoint) {
        countyDataService.getData($scope.dataPoint).then(function(countyData) {
          drawMap.setCurrentData(countyData, 1);
            stateFips.forEach(function(fips) {
              drawMap.visualizeDataForState(fips, 1);
            })
          
        });
      }
      
    });

    $scope.$watch('dataPoint2', function() {
      if ($scope.dataPoint2) {
        countyDataService.getData($scope.dataPoint2).then(function(countyData) {
          drawMap.setCurrentData(countyData, 2);
          stateFips.forEach(function(fips) {
            drawMap.visualizeDataForState(fips, 2);
          })
        });
      }
      
    });

    
    

    $scope.drawMap = drawMap;

  }]);
