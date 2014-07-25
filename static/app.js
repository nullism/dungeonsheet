var DNDApp = angular.module('DNDApp', []);
 
DNDApp.controller('StatsController', function($scope, $http) {

    $http.get('/stats.json')
       .then(function(res){
          $scope.stats = res.data; 
          $scope.stats.spells.predicate = 'level';
    });

    $scope.sortSkills = function(how) {       
        $scope.stats.skills.predicate = how;
    }

    $scope.resetSkills = function() { 
        if(!$scope.stats) { return 0; }
        var okay = confirm("Are you sure?");
        if(!okay) { return 0; }
        $http.get('/stats.json?resetSkills=True')
            .then(function(res) {
              $scope.stats.skills = res.data.skills;
        });
    }

    $scope.save = function() { 
        var jstats = $("#stats_json").text();
        //console.log('Saving data...');
        //console.log(jstats);
        $http.post('/stats.json/save', {"stats":jstats});
    }

    $scope.addAttack = function() { 
        if(!$scope.stats) { return 0; }
        $scope.stats.attacks.push({"damage":"1d3"});
    }

    $scope.removeAttack = function(idx) { 
        if(!$scope.stats) { return 0; }
        var okay = confirm("Are you sure?");
        if(!okay) { return 0; }
        $scope.stats.attacks.splice(idx, 1);
    }


    $scope.addItem = function() { 
        if(!$scope.stats) { return 0; }
        $scope.stats.items.push({"weight":0, "quantity":1});
    }

    $scope.removeItem = function(idx) { 
        if(!$scope.stats) { return 0; }
        var okay = confirm("Are you sure?");
        if(!okay) { return 0; }
        $scope.stats.items.splice(idx, 1);
    }

    $scope.addFeat = function() { 
        if(!$scope.stats) { return 0; }
        $scope.stats.feats.push({});
    }

    $scope.removeFeat = function(idx) { 
        if(!$scope.stats) { return 0; }
        var okay = confirm("Are you sure?");
        if(!okay) { return 0; }
        $scope.stats.feats.splice(idx, 1);
    }

    $scope.addLanguage = function() { 
        if(!$scope.stats) { return 0; }
        $scope.stats.languages.push({});
    }

    $scope.removeLanguage = function(idx) { 
        if(!$scope.stats) { return 0; }
        var okay = confirm("Are you sure?");
        if(!okay) { return 0; }
        $scope.stats.languages.splice(idx, 1);
    }

    $scope.addSpecialAbility = function() { 
        if(!$scope.stats) { return 0; }
        $scope.stats.special_abilities.push({});
    }

    $scope.removeSpecialAbility = function(idx) { 
        if(!$scope.stats) { return 0; }
        var okay = confirm("Are you sure?");
        if(!okay) { return 0; }
        $scope.stats.special_abilities.splice(idx, 1);
    }

    $scope.addSpell = function() { 
        if(!$scope.stats) { return 0; }
        $scope.stats.spells.push({"level":0});
    }

    $scope.removeSpell = function(spell_name) { 
        if(!$scope.stats) { return 0; }
        var okay = confirm("Are you sure?");
        if(!okay) { return 0; }
        for(var i=0; i<$scope.stats.spells.length; i++) {
            var sp = $scope.stats.spells[i];
            if(sp.name == spell_name) { 
                $scope.stats.spells.splice(i, 1);
                break;
            }
        }
    }



    $scope.getAbilityMod = function(stat) {
        var statmod = stat - 10;
        if(statmod > 0) { 
            return Math.floor(statmod / 2);
        }  
            
        return Math.ceil(statmod / 2);
    };

    $scope.getFortitude = function() { 
        if(!$scope.stats) {
            return 0;
        }
        return parseInt($scope.stats.base_fort_save) 
            + $scope.getAbilityMod($scope.stats.abilities[2].value)
            + parseInt($scope.stats.magic_fort_mod)
            + parseInt($scope.stats.misc_fort_mod);
    }

    $scope.getReflex = function() { 
        if(!$scope.stats) {
            return 0;
        }
        return parseInt($scope.stats.base_ref_save) 
            + $scope.getAbilityMod($scope.stats.abilities[1].value)
            + parseInt($scope.stats.magic_ref_mod)
            + parseInt($scope.stats.misc_ref_mod);
    }

    $scope.getWill = function() { 
        if(!$scope.stats) {
            return 0;
        }
        return parseInt($scope.stats.base_will_save) 
            + $scope.getAbilityMod($scope.stats.abilities[4].value)
            + parseInt($scope.stats.magic_will_mod)
            + parseInt($scope.stats.misc_will_mod);
    }

    $scope.getInitiative = function() { 
        if(!$scope.stats) { 
            return 0;
        }
        return parseInt($scope.stats.initiative_mod) + parseInt($scope.getAbilityMod($scope.stats.abilities[1].value));
    
    };

    $scope.getAC = function() {
        if(!$scope.stats) { 
            return 0;
        }
        return 10 + ($scope.getAbilityMod($scope.stats.abilities[1].value) 
            + parseInt($scope.stats.armor_bonus)
            + parseInt($scope.stats.shield_bonus)
            + parseInt($scope.stats.size_ac_mod)
            + parseInt($scope.stats.natural_armor)
            + parseInt($scope.stats.deflection_mod)
            + parseInt($scope.stats.misc_ac_mod));
    };

    $scope.getTouchAC = function() { 
        if(!$scope.stats) { return 0; }
        return 10 + ($scope.getAbilityMod($scope.stats.abilities[1].value) 
            + parseInt($scope.stats.size_ac_mod)
            + parseInt($scope.stats.deflection_mod)
            + parseInt($scope.stats.misc_ac_mod));
    }

    $scope.getSkillTotal = function(skill) { 
        if(!$scope.stats) { 
            return 0;
        }
        return $scope.getAbilityMod($scope.stats.abilities[skill.ability_index].value)
            + parseInt(skill.ranks) + parseInt(skill.misc_mod);
    }

    $scope.getItemWeightTotal = function() { 
        if(!$scope.stats) {
            return 0;
        }
        var totalWeight = 0;
        for(var i=0; i<$scope.stats.items.length; i++) { 
            var item = $scope.stats.items[i];
            totalWeight += parseInt(item.weight) * parseInt(item.quantity);
        }
        return totalWeight;
    }

});



