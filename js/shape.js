// Check if a point is inside a polygon
// TODO: revise
//
var Shape = function Shape(nodes) {
	/* nodes in the order in which they are to be connected */

	/* Functions responsible for working out whether a node
	 * satisfies an inequality */
	var less = function(edge,item){return item.y<right(edge,item.x)};
	var greater = function(edge,item){return item.y>right(edge,item.x)};
	var right = function(edge,x){
		return ((edge[1].y-edge[0].y)/(edge[1].x-edge[0].x))
			*(x-edge[0].x)+edge[0].y;};

	this.inequalities = []

	/* The sign for which the highest no. of nodes satisfy the
	 * inequality is selected */
	var getInequality = function getInequality(edge){
		var less_no = nodes.filter(function(node_){
			return less(edge,node_);}).length;
		var greater_no = nodes.filter(function(node_){
			return greater(edge,node_);}).length;
		return [edge,less_no>greater_no?less:greater];
	}
	/* Pair all nodes next to each other to form edges */
	for (var i = 1; i<nodes.length;i++){
		var edge = [nodes[i-1],nodes[i]];
		this.inequalities.push(getInequality(edge));
	}
	this.inequalities.push(getInequality([nodes[0],nodes[nodes.length-1]]));
}

Shape.prototype.check = function check(node) {
	var passed = this.inequalities.filter(function(ineq){
		return ineq[1](ineq[0],node);
	}).length;
	return (passed/this.inequalities.length)>0.5;
}


var a = new Shape([{x:0,y:0},{x:10,y:0},{x:10,y:10},{x:4,y:3},{x:4,y:6},{x:3,y:10}]);
console.log(a.check({x:1,y:1}));
