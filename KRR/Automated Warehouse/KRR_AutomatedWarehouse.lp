%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CSE 579 : Knowledge Representation And Reasoning
% FileName: AutomatedWarehouse.lp
% Session: Spring A
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Convert data to input 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Number of Row in the grid
rowNum(row):- row=#count{Y:init(object(node,I),value(at,pair(X,Y)))}.

% Number of column in the grid
colNum(col):- col=#count{X:init(object(node,I),value(at,pair(X,Y)))}.

% Number of robot in the system
roboNum(RC):- RC=#count{I:init(object(robot,I),value(at,pair(X,Y)))}.

% Determine the node type(Regular , Highway)
node(NodeId):- init(object(node,NodeId),value(at,pair(X,Y))).
nodeAt(NodeId,pair(X,Y)):- init(object(node,NodeId),value(at,pair(X,Y))).
highway(NodeId):- init(object(highway,NodeId),value(at,pair(X,Y))).

% Picking Station details
pickingStation(PSID):- init(object(pickingStation,PSID),value(at,pair(X,Y))), init(object(node,NodeId),value(at,pair(X,Y))).
pickingStationAt(PSID,NodeId):- init(object(pickingStation,PSID),value(at,pair(X,Y))), init(object(node,NodeId),value(at,pair(X,Y))).

% Robot Details
robot(RID):- init(object(robot,RID),value(at,pair(X,Y))).

% Shelf Details
slf(SLFID):- init(object(slf,SLFID),value(at,pair(X,Y))).

% Robot and Shelf location at initial state
roboLoc(RID,object(node,NodeId),1):- init(object(robot,RID),value(at,pair(X,Y))), nodeAt(NodeId,pair(X,Y)).
shelfLoc(SLFID,object(node,NodeId),1):- init(object(slf,SLFID),value(at,pair(X,Y))), nodeAt(NodeId,pair(X,Y)).

%Product Details
prodDetails(Product,object(slf,SLFID),with(quantity,ProdQTY),1):- init(object(product,Product),value(on,pair(SLFID,ProdQTY))).

% Initial Product and Order Details
orderDetails(OID,object(node,ND),contains(Product,ProdQTY),1):- init(object(order,OID),value(pickingStation,PKI)), pickingStationAt(PKI,ND), init(object(order,OID),value(line,pair(Product,ProdQTY))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Actions Details
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
move(0,1;0,-1;-1,0;1,0).
{robotMove(R,move(P,Q),I):move(P,Q)}1:- R=1..RC, roboNum(RC), I=1..m.
{pickUpShelf(R,SLFID,I):slf(SLFID)}1:- R=1..RC, roboNum(RC), I=1..m.
{putDownShelf(R,SLFID,I):slf(SLFID)}1:- R=1..RC, roboNum(RC), I=1..m.
{deliveryDetails(R,OID,with(SLFID,PROD,DelQ),I):orderDetails(OID,object(node,ND),contains(PROD,Order),I), prodDetails(PROD,object(slf,SLFID),with(quantity,ProdQTY),I), DelQ=1..ProdQTY}1:- R=1..RC, roboNum(RC), I=1..m.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Output Details
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
occurs(object(robot,R),move(P,Q),I):-robotMove(R,move(P,Q),I), I=1..m.
occurs(object(robot,R),pickup,I):-pickUpShelf(R,_,I), I=1..m.
occurs(object(robot,R),putdown,I):-putDownShelf(R,_,I), I=1..m.
occurs(object(robot,R),deliver(OID,Product,DelQ),I):-deliveryDetails(R,OID,with(SLFID,Product,DelQ),I), I=1..m.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Constraints On Action
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Two actions can't occur at the same time
:- occurs(object(robot,R),Action1,I), occurs(object(robot,R),Action2,I), Action1!=Action2 , I=1..m.

%%%%%%%%%%%%%%	Move constraints %%%%%%%%%%%%%%
% Robot can move within the defined grid of warehouse
:- roboLoc(R,object(node,ND),I), robotMove(R,move(P,Q),I), nodeAt(ND,pair(X,Y)), X+P<1 , I=1..m.
:- roboLoc(R,object(node,ND),I), robotMove(R,move(P,Q),I), nodeAt(ND,pair(X,Y)), Y+Q<1 , I=1..m.
:- roboLoc(R,object(node,ND),I), robotMove(R,move(P,Q),I), nodeAt(ND,pair(X,Y)), X+P>col, colNum(col) , I=1..m.
:- roboLoc(R,object(node,ND),I), robotMove(R,move(P,Q),I), nodeAt(ND,pair(X,Y)), Y+Q>row, rowNum(row) , I=1..m.

%%%%%%%%%%%%%% PickUpShelf constraint %%%%%%%%%%%%%%
%Robot and Node containing slf should be at same place
:- pickUpShelf(R,S,I), shelfLoc(S,object(node,ND),I), not roboLoc(R,object(node,ND),I), I=1..m. 
% One Robot can pickup a slf at one time (i.e.Multiple robort can't pich the same slf)
:- pickUpShelf(R1,S,I), shelfLoc(S,object(robot,R2),I), I=1..m.

%%%%%%%%%%%%%%	PutDownShelf constraint	%%%%%%%%%%%%%%
% Robot can putdown one slf
:- putDownShelf(R,S,I), not shelfLoc(S,object(robot,R),I), I=1..m.
% Robot can't putdown a slf on highway
:- putDownShelf(R,S,I), roboLoc(R,object(node,ND),I), highway(ND), I=1..m.
% Robot can't putdown slf on picking station
:- putDownShelf(R,S,I), roboLoc(R,object(node,ND),I), pickingStationAt(_,ND), I=1..m.

%%%%%%%%%%%%%%	Delivery constraint	%%%%%%%%%%%%%%
% For delivery robot should be at picking station
:- deliveryDetails(R,OID,with(_,PQ,_),I), orderDetails(OID,object(node,ND),contains(PQ,_),I), not roboLoc(R,object(node, ND),I), I=1..m.
% For delivery robot should have slf having correct product
:- deliveryDetails(R,OID,with(SLFID,PQ,_),I), prodDetails(PQ,object(slf,SLFID),with(quantity,_),I), not shelfLoc(SLFID,object(robot,R),I), I=1..m.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Constraint On State 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Can't put Shelf on a highway.
:- shelfLoc(S,object(node,NodeId),_), highway(NodeId).

:- not {roboLoc(R,object(node,ND),I):node(ND)}1, robot(R), I=1..m+1.

% Same node doesn't have multiple robot
:- not {roboLoc(R,object(node,ND),I):robot(R)}1, node(ND), I=1..m+1.

% Robots can't swap location
:- roboLoc(R1,object(node,N1),I), roboLoc(R1,object(node,N),I+1), roboLoc(R2,object(node,N),I), roboLoc(R2,object(node,N1),I+1), R1!=R2, I=1..m+1.

% Shelf has only one robot
%:- not{shelfLoc(S,object(robot,NR),I): robot(NR)}1, slf(S), I=1..m+1.
:- shelfLoc(S,object(robot,R1),I), shelfLoc(S,object(robot,R2),I), R1!=R2, I=1..m+1.

% Robot has only one slf
:- not{shelfLoc(S,object(robot,NR),I): slf(S)}1, robot(NR), I=1..m+1.

% Shelf contain only one nodes
:- not{shelfLoc(S,object(node,ND),I): node(ND)}1, slf(S), I=1..m+1.

% One node has only one slf
:- not{shelfLoc(S,object(node,ND),I): slf(S)}1, node(ND), I=1..m+1.

% Robot having slf can't move to a cell which is having slf 
:- shelfLoc(S1,object(robot,R),I),roboLoc(R,object(node,N),I+1), shelfLoc(S2,object(node,N),I+1),S1!=S2, not pickingStationAt(_,N), I=1..m+1.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Effect on Action
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Move
roboLoc(R,object(node,N),I+1):- roboLoc(R,object(node,N1),I), nodeAt(N1,pair(X,Y)), nodeAt(N, pair(X+P,Y+Q)), robotMove(R,move(P,Q),I), I=1..m.

% PickUpShelf
shelfLoc(S,object(robot,R),I+1):- pickUpShelf(R,S,I), shelfLoc(S,object(node,ND),I), roboLoc(R,object(node,ND),I), I=1..m.

% PutDownShelf
shelfLoc(S,object(node,ND),I+1):- putDownShelf(R,S,I), shelfLoc(S,object(robot,R),I), roboLoc(R,object(node,ND),I), I=1..m.

% Delivery Details
orderDetails(OID,object(node,ND),contains(PROD,OrdQ-DelQ),I+1):- deliveryDetails(R,OID,with(SLFID,PROD,DelQ),I), orderDetails(OID,object(node,ND),contains(PROD,OrdQ),I), I=1..m.
prodDetails(PROD,object(slf,SLFID),with(quantity,ProdQTY-DelQ),I+1):- deliveryDetails(R,OID,with(SLFID,PROD,DelQ),I), prodDetails(PROD,object(slf,SLFID),with(quantity,ProdQTY),I), I=1..m.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 					Law of Intertia
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
roboLoc(R,object(node,ND),I+1):- roboLoc(R,object(node,ND),I), not robotMove(R,move(_,_),I), I=1..m.
shelfLoc(S,object(node,ND),I+1):-shelfLoc(S,object(node,ND),I), not pickUpShelf(_,S,I), I=1..m.
shelfLoc(S,object(robot,R),I+1):-shelfLoc(S,object(robot,R),I), not putDownShelf(R,S,I), I=1..m.
orderDetails(OID,object(node,ND),contains(PROD,OrdQ),I+1):- orderDetails(OID,object(node,ND),contains(PROD,OrdQ),I), prodDetails(PROD,object(slf,SLFID),with(quantity,ProdQTY),I), not deliveryDetails(_,OID,with(SLFID,PROD,_),I), I=1..m.
prodDetails(PROD,object(slf,SLFID),with(quantity,ProdQTY),I+1):- prodDetails(PROD,object(slf,SLFID),with(quantity,ProdQTY),I), not deliveryDetails(_,_,with(SLFID,PROD,_),I), I=1..m.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Goal
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
:- not orderDetails(OID,object(node,_),contains(PQ,0),m+1), orderDetails(OID,object(node,_),contains(PQ,_),1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	
% Calculation of Time and action
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
actions(N) :- N=#count{1,R,A,I:occurs(R,A,I)}.
time(N) :- N=#count{I:occurs(R,A,I)}.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Optimization
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Minimum time taken to fulfill order
%#minimize{I:occurs(R,A,I)}.
#minimize { 1,R,A,I : occurs(R,A,I)}.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Output
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#show occurs/3.
#show actions/1.
#show time/1.
