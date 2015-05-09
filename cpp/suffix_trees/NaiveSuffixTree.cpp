#include "NaiveSuffixTree.h"
#include <string>
#include <iostream>

NaiveSuffixTree::NaiveSuffixTree(std::string str) 
    : root_(new Node), str(str) {
    build();
}
Node* NaiveSuffixTree::root() {
    return root_;
}
const std::string NaiveSuffixTree::text() {
    return str;
}
void NaiveSuffixTree::insert_suffix(int start, int end) {
    std::vector<Node*> m = root_->children;
    for (auto it = m.begin(); it != m.end(); it++) {
        Node *child = *it;
        int i = 0;
        // Intentionally case-sensitive
        while (str[start+i] == str[child->start+i]) {
            i++;
        }
        if (i > 0) {
            Node *nodeB = new Node;
            nodeB->start = (*it)->start + i;
            nodeB->end =  (*it)->end;
            nodeB->value = (*it)->start;

            //   R               R
            //  /     becomes   /
            // A               A
            //                / \
            //                B  C
            //
            // A splits into A and B
            (*it)->end = (*it)->start + i - 1;
            // A and B swap their children
            std::swap((*it)->children,nodeB->children);
            // B is newly created and has no children
            // After this B will have all of A's children and A's new
            // set of children becomes empty so we add B to it
            (*it)->children.push_back(nodeB);

            Node *nodeC = new Node;
            nodeC->value = start;
            nodeC->start = start+i;
            nodeC->end = end;
            (*it)->children.push_back(nodeC);
            return;
        }
    }

    Node *new_node = new Node;
    new_node->start = start;
    new_node->value = start;
    new_node->end = end;
    root_->children.push_back(new_node);
}
void NaiveSuffixTree::build() {
    // Insert all suffixes
    for (int i = 0; i < str.size(); i++) {
        insert_suffix(i,str.size()-1);
    }
}

void NaiveSuffixTree::display() {
    if (root_->children.empty()) {
        std::cout << "Empty tree" << std::endl;
    } else {
        display(root_,0);
    }
}
void NaiveSuffixTree::display(Node *tmp_node, int depth) {
    std::vector<Node*> *m = &tmp_node->children;

    for (auto it = m->begin(); it != m->end(); ++it) {
        Node *node = *it; 
        std::cout 
            << std::string(depth,'-')
            << "[" << it-m->begin()+1 << "]"
            << str.substr(node->start,node->end - node->start+1) 
            << std::endl;

        if (!node->children.empty()) {
            display(node,depth+1);
        }
    }
}
