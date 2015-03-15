/**
 * Created by Mihail on 14.03.15.
 */

app.controller('LeftSidebarController', function ($scope) {
    $scope.set_active = function($event) {

        // set all sidebar items to unactive
        var left_sidebar = document.getElementById("left_sidebar");
        var li_elems = left_sidebar.getElementsByTagName("li");
        for (var i = 0; i < li_elems.length; i++) {
            li_elems[i].classList.remove("active");
        }

        // set current sidebar item active
        $event.target.parentNode.classList.add("active");
    }

    $scope.ccclick = function($event) {
        console.log($event.target);
    }
});