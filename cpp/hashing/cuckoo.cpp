#include <iostream>
#include <functional>
#include <stdio.h>
#include <cstring>
#include <cstdlib>
#include <vector>

unsigned long djb2(const char *str) {
    unsigned long hash = 5381;
    int c;

    while (c = *str++)
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    return hash;
}
unsigned long sdbm(const char *str) {
    unsigned long hash = 0;
    int c;

    while (c = *str++)
        hash = c + (hash << 6) + (hash << 16) - hash;

    return hash;
}


typedef struct position_ {
    unsigned int index;
    bool vacant;
    char *key;
} Position;

class Cuckoo {
    public:
        Cuckoo(int size) : size(size) {
            table = static_cast<int*>(calloc(size,sizeof(int)));
            ids = static_cast<char**>(calloc(size,sizeof(char*)));
            for(int i = 0; i < size; i++) {
                table[i] = -1;
                ids[i] = static_cast<char*>(calloc(20,sizeof(char)));
            }
            hash1_ub = &sdbm;
            hash2_ub = &djb2;
        }

        void insert(const char* key, int val);
        void insert(const char* key, int val, int depth);
        void shuffle_insert(const char* key, int val);
        int lookup(const char* key);
        void remove(const char* key);
        void print();
        void positions(Position *posa, const char* key);
    private:
        unsigned long(*hash1_ub)(const char*);
        unsigned long(*hash2_ub)(const char*);

        /* Bound versions */
        unsigned int hash1(const char*);
        unsigned int hash2(const char*);

        int size;
        int *table;
        char **ids;
};

unsigned int Cuckoo::hash1(const char* str) {
    if (hash1_ub == NULL) {
        return -1;
    }
    return (*hash1_ub)(str) % size;
}

unsigned int Cuckoo::hash2(const char* str) {
    if (hash2_ub == NULL) {
        return -1;
    }
    return (*hash2_ub)(str) % size;
}

void Cuckoo::insert(const char* key, int val) {
    this->insert(key,val,0);
}

void Cuckoo::positions(Position *posa, const char* key) {
    unsigned int h1r = hash1(key), h2r = hash2(key);
    posa[0].key = ids[h1r];
    posa[0].index = h1r;
    posa[0].vacant = strcmp(ids[h1r],"") == 0;

    posa[1].key = ids[h2r];
    posa[1].index = h2r;
    posa[1].vacant = strcmp(ids[h2r],"") == 0;
}
void Cuckoo::shuffle_insert(const char* key, int val) {
    Position positions_x[2];
    Position positions_h1act[2];
    Position positions_h2act[2];

    positions(positions_x,key);
    positions(positions_h1act,positions_x[0].key);
    positions(positions_h2act,positions_x[1].key);
    printf("position_x[0]=%d\n",positions_x[0].index);
}
void Cuckoo::remove(const char* key) {
    Position positions_x[2];
    positions(positions_x,key);
    if (strcmp(positions_x[0].key,key)==0) {
        memset(ids[positions_x[0].index],0,20);
    } else if (strcmp(positions_x[1].key,key)==0) {
        memset(ids[positions_x[1].index],0,20);
    } else {
        printf("Cannot remove %s - not found\n",key);
    }
}
void Cuckoo::insert(const char* key, int val, int depth) {
    Position positions_x[2];
    positions(positions_x,key);
    printf("Insert(%d) [%s=%d] \t\t\t-\t\t\t [ind=%d|%s] [ind=%d|%s]\n",depth,key,val,positions_x[0].index,positions_x[0].key,
            positions_x[1].index,positions_x[1].key);

    unsigned int h1r = hash1(key), h2r = hash2(key);
    //printf("h1: %d, h2: %d - for [key=%s]\n",h1r,h2r,key);

    if (positions_x[0].vacant) {
        table[h1r] = val;
        //printf("about to copy key [%s] into [index=%d] to replace [%s]\n",key,h1r,ids[h1r]);
        strcpy(ids[h1r],key);
    } else if (positions_x[1].vacant) {
        table[h2r] = val;
        strcpy(ids[h2r],key);
    } else {
        if (depth == size) {
            // rebuild
            printf("REBUILD!\n");
            print();
            exit(0);
        } else {
            // shuffle
            char *h1key = static_cast<char*>(calloc(20,sizeof(char)));
            strcpy(h1key,positions_x[0].key);

            int h1aval = this->lookup(h1key);
            this->remove(h1key);
            this->insert(key,val,depth+1);
            printf("|-- reinsert [%s=%d]\n",h1key,h1aval);
            this->insert(h1key,h1aval,depth+1);
            free(h1key);
        }
    }
    //printf("id: %s\n",ids[h1r]);
}

void Cuckoo::print() {
    printf("index,key,value\n");
    for (int i = 0; i < size; i++) {
        printf("%d,%s,%d\n",i,ids[i],table[i]);
    }
}

int Cuckoo::lookup(const char* key) {
    Position x[2];
    positions(x,key);

    if(strcmp(x[0].key,key)==0) {
        return table[x[0].index];
    } else if (strcmp(x[1].key,key)==0) {
        return table[x[1].index];
    } else {
        printf("Key [%s] not found\n",key);
        return -1;
    }
}

int main(int argc, const char *argv[])
{
    Cuckoo c(100);
    char str[] = "tes00";
    for (int i = 0; i < 50; i++) {
        str[3] = '0' + i / 10;
        str[4] = '0' + i % 10;
        str[1] += ((i % 2)*2 - 1);
        str[0] += ((i % 5) - 2);
        str[2] --;
        c.insert(str,i);
    }
    //const unsigned char* str2 = reinterpret_cast<const unsigned char*>(str);
    //std::cout << hash1("test") << std::endl; 
    return 0;
}
