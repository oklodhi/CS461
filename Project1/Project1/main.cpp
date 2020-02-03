// Omer Khan
// CS461 Project 1
// Brian Hare T/Th 1-2:15pm 
// Febuary 9, 2020

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std; 

// class tree based on game board
class State_Tree {
private: 
	struct Node {
		Node * parent;

		Node * node1;
		Node * node2;
		Node * node3;
		Node * node4;

		vector<int> board; 

		int index; 
		int distance; 
		int cost;
	};

	vector<Node*> S; 

	vector<int> initial_state;
	vector<int> goal_state; 

	Node* r; 

	int height; 
	bool g; 

public: 
	State_Tree() {
		r = NULL;
	}

	// Functions 
	void create_root(vector<int>);
	void create();
	void insert(Node*);
	void input_state(string FILENAME);
	void print_state(Node*);
	void shift(Node*, Node*, char);
	void check_goal(Node*);
	void sort();
	int s1(Node*);

	bool isEmpty() const
	{
		return r == NULL;
	}
};

// create root of tree
void State_Tree::create_root(vector<int> board)
{
	Node* n1 = new Node;

	for (int i = 0; i < (signed)board.size(); i++)
	{
		n1->board.push_back(board[i]);
	}

	n1->cost = s1(n1);
	n1->distance = 1;

	n1->parent = NULL;
	n1->node1 = NULL;
	n1->node2 = NULL;
	n1->node3 = NULL;
	n1->node4 = NULL;

	for (int i = 0; i < (signed)board.size(); i++)
	{
		if (board[i] == 0)
		{
			n1->index = i;
		}
	}

	if (isEmpty())
	{
		r = n1;
		S.push_back(r);
	}
}

// Generate tree
void State_Tree::create()
{
	input_state();
	create_root(initial_state);
	g = false;

	Node* current;
	height = 1;

	int t = 0;

	while (S.size() > 0)
	{
		current = S.front();
		S.erase(S.begin());
		insert(current);

		if (current->distance > t)
		{
			t = current->distance;
		}
	}
}

// insert nodes into tree
void State_Tree::insert(Node* current)
{
	Node* n1 = new Node;
	shift(current, n1, 'u');
	n1->distance = current->distance + 1;
	n1->cost = s1(n1) + n1->distance;
	n1->parent = current;
	n1->node1 = NULL;
	n1->node2 = NULL;
	n1->node3 = NULL;
	n1->node4 = NULL;

	Node* n2 = new Node;
	shift(current, n2, 'r');
	n2->distance = current->distance + 1;
	n2->cost = s1(n2) + n2->distance;
	n2->parent = current;
	n1->node1 = NULL;
	n1->node2 = NULL;
	n1->node3 = NULL;
	n1->node4 = NULL;

	Node* n3 = new Node;
	shift(current, n3, 'd');
	n3->distance = current->distance + 1;
	n3->cost = s1(n3) + n3->distance;
	n3->parent = current;
	n1->node1 = NULL;
	n1->node2 = NULL;
	n1->node3 = NULL;
	n1->node4 = NULL;

	Node* n4 = new Node;
	shift(current, n4, 'l');
	n4->distance = current->distance + 1;
	n4->cost = s1(n4) + n4->distance;
	n4->parent = current;
	n1->node1 = NULL;
	n1->node2 = NULL;
	n1->node3 = NULL;
	n1->node4 = NULL;

	if ((current->node1 == NULL) && (n1->board.size() > 0))
	{
		current->node1 = n1;
		if (!g)
			S.push_back(current->node1);
	}
	else
		delete n1;

	if ((current->node2 == NULL) && (n2->board.size() > 0))
	{
		current->node2 = n2;
		if (!g)
			S.push_back(current->node2);
	}
	else
		delete n2;

	if ((current->node3 == NULL) && (n3->board.size() > 0))
	{
		current->node3 = n3;
		if (!g)
			S.push_back(current->node3);
	}
	else
		delete n3;

	if ((current->node4 == NULL) && (n4->board.size() > 0))
	{
		current->node4 = n4;
		if (!g)
			S.push_back(current->node4);
	}
	else
		delete n4;

	sort();
	check_goal(current);
}

// shifts block positions in the grid
void State_Tree::shift(Node* current, Node* n, char c)
{
	int a, index;
	bool f = false;

	for (int i = 0; i < (signed)current->board.size(); i++)
	{
		if (current->board[i] == 0)
		{
			index = i;
		}
		n->board.push_back(current->board[i]);
	}

	n->index = index;

	if (current->distance > 2)
	{
		if (index == current->parent->index)
		{
			f = true;
		}
	}


	switch (c)
	{
	case 'r':
		if ((index % 3 != 2) && (!f))
		{
			a = n->board[index];
			n->board[index] = n->board[index + 1];
			n->board[index + 1] = a;
		}
		else
			n->board.erase(n->board.begin(), n->board.end());
		break;
	case 'l':
		if ((index % 3 != 0) && (!f))
		{
			a = n->board[index];
			n->board[index] = n->board[index - 1];
			n->board[index - 1] = a;
		}
		else
			n->board.erase(n->board.begin(), n->board.end());
		break;
	case 'u':
		if ((index > 2) && (!f))
		{
			a = n->board[index];
			n->board[index] = n->board[index - 3];
			n->board[index - 3] = a;
		}
		else
			n->board.erase(n->board.begin(), n->board.end());
		break;
	case 'd':
		if ((index < 6) && (!f))
		{
			a = n->board[index];
			n->board[index] = n->board[index + 3];
			n->board[index + 3] = a;
		}
		else
			n->board.erase(n->board.begin(), n->board.end());
		break;
	}
}

// Inputting Initial and final states from Input File
void State_Tree::input_state(string FILENAME)
{	
	int x = 0;
	puzzle_Grid.resize(3);
	for (int row = 0; row < 3; row++) {
		puzzle_Grid[row].resize(3);
		for (int col = 0; col < 3; col++) {
			stream >> x;
			puzzle_Grid[row][col] = x;
			cout << puzzle_Grid[row][col] << " ";
		}
		cout << endl;
	}

	stream.close();

	ifstream stream("program1_output.txt");

	string p, q;
	int n = 0;

	while (getline(in, p))
	{
		istringstream linestream(p);

		while (getline(linestream, q, ' '))
		{
			n++;

			if (n <= 9)
			{
				initial_state.push_back(atoi(q.c_str()));
			}
			else
			{
				goal_state.push_back(atoi(q.c_str()));
			}
		}
	}
}

void State_Tree::print_state(Node* n)
{
	vector<Node*> v;
	ofstream out("output.txt");

	while (n != NULL)
	{
		v.push_back(n);
		n = n->parent;
	}
	for (int b = v.size() - 1; b >= 0; b--)
	{
		for (int a = 0; a < (signed)v[b]->board.size(); a++)
		{
			out << v[b]->board[a] << " ";
			cout << v[b]->board[a] << " ";

			if (a % 3 == 2)
			{
				out << endl;
				cout << endl;
			}
		}
		out << endl;
		cout << endl;
	}
	cout << "Goal state achieved." << endl;

	ifstream infile("output.txt");
	ofstream ofile("program1_output.txt");

	int arr[10], arr1[10], arr2[10], arr3[10], arr4[10];
	int l = 0, m = 0, g = 0, p = 0, q = 0;

	for (int i = 0; i < 9; i++)
	{
		infile >> arr[i];

		if (arr[i] == 0)
		{
			l = i;
		}
	}

	for (int i = 0; i < 9; i++)
	{
		infile >> arr1[i];

		if (arr1[i] == 0)
		{
			m = i;
		}
	}

	for (int i = 0; i < 9; i++)
	{
		infile >> arr2[i];

		if (arr2[i] == 0)
		{
			g = i;
		}
	}

	for (int i = 0; i < 9; i++)
	{
		infile >> arr3[i];

		if (arr3[i] == 0)
		{
			p = i;
		}
	}

	for (int i = 0; i < 9; i++)
	{
		infile >> arr4[i];

		if (arr4[i] == 0)
		{
			q = i;
		}
	}

	if (m == l + 1)
	{
		ofile << arr[m] << " left" << endl;
	}
	else if (m == l + 3)
	{
		ofile << arr[m] << " up" << endl;
	}

	if (g == m + 1)
	{
		ofile << arr1[g] << " left" << endl;
	}
	else if (g == m + 3)
	{
		ofile << arr1[g] << " up" << endl;
	}
	else if (g == m - 3)
	{
		ofile << arr1[g] << " down" << endl;
	}
	else if (g == m - 1)
	{
		ofile << arr1[g] << " right" << endl;
	}

	if (p == g + 1)
	{
		ofile << arr2[p] << " left" << endl;
	}
	else if (p == g + 3)
	{
		ofile << arr2[p] << " up" << endl;
	}
	else if (p == g - 3)
	{
		ofile << arr2[p] << " down" << endl;
	}
	else if (p == g - 1)
	{
		ofile << arr2[p] << " right" << endl;
	}

	if (q == p + 1)
	{
		ofile << arr3[q] << " left" << endl;
	}
	else if (q == p + 3)
	{
		ofile << arr3[q] << " up" << endl;
	}
	else if (q == p - 3)
	{
		ofile << arr3[q] << " down" << endl;
	}
	else if (q == p - 1)
	{
		ofile << arr3[q] << " right" << endl;
	}

	ofile << "Goal state found." << endl;

	out.close();
}

int State_Tree::s1(Node* n)
{
	int q = 0;

	for (int a = 0; a < (signed)n->board.size(); a++)
	{
		if (n->board[a] != goal_state[a])
		{
			q++;
		}
	}

	return q;
}

void State_Tree::sort()
{
	Node* n;

	for (int i = 0; i < (signed)S.size() - 1; i++)
	{
		for (int j = 0; j < (signed)S.size() - 1; j++)
		{
			if (S[j]->cost > S[j + 1]->cost)
			{
				n = S[j];
				S[j] = S[j + 1];
				S[j + 1] = n;
			}
		}
	}
}

//To check whether we reach the goal or not.
void State_Tree::check_goal(Node* curr)
{
	bool check1 = true, check2 = true, check3 = true, check4 = true;

	for (int a = 0; a < (signed)goal_state.size(); a++)
	{
		if (curr->node1 != NULL)
		{
			if (curr->node1->board[a] != goal_state[a])
				check1 = false;
		}
		else
			check1 = false;

		if (curr->node2 != NULL)
		{
			if (curr->node2->board[a] != goal_state[a])
				check2 = false;
		}
		else
			check2 = false;

		if (curr->node3 != NULL)
		{
			if (curr->node3->board[a] != goal_state[a])
				check3 = false;
		}
		else
			check3 = false;

		if (curr->node4 != NULL)
		{
			if (curr->node4->board[a] != goal_state[a])
				check4 = false;
		}
		else
			check4 = false;
	}

	if (check1)
	{
		g = true;
		print_state(curr->node1);
	}
	else if (check2)
	{
		g = true;
		print_state(curr->node2);
	}
	else if (check3)
	{
		g = true;
		print_state(curr->node3);
	}
	else if (check4)
	{
		g = true;
		print_state(curr->node4);
	}

	if (g)
	{
		while (!S.empty())
		{
			S.erase(S.begin());
		}
	}
}



int main()
{
	State_Tree tree;
	tree.create();

	system("pause");
	return 0;
}