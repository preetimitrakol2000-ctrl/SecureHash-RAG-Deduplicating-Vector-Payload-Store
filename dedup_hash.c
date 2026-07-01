#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define VAULT_CAPACITY 31

typedef struct {
    char entry_hash[64];
    int mapped_document_id;
} HashEntry;

typedef struct {
    HashEntry table[VAULT_CAPACITY];
    int element_count;
} DedupTable;

unsigned int calculate_simple_hash(const char* str) {
    unsigned int hash = 0;
    while (*str) hash = (hash * 31) + *str++;
    return hash % VAULT_CAPACITY;
}

#ifdef _WIN32
    __declspec(dllexport) DedupTable* init_table();
    __declspec(dllexport) int register_document_payload(DedupTable* dt, const char* text_hash, int doc_id);
    __declspec(dllexport) void clear_table(DedupTable* dt);
#endif

DedupTable* init_table() {
    DedupTable* dt = (DedupTable*)malloc(sizeof(DedupTable));
    dt->element_count = 0;
    for (int i = 0; i < VAULT_CAPACITY; i++) {
        strcpy(dt->table[i].entry_hash, "");
        dt->table[i].mapped_document_id = -1;
    }
    return dt;
}

int register_document_payload(DedupTable* dt, const char* text_hash, int doc_id) {
    unsigned int slot = calculate_simple_hash(text_hash);
    int initial_slot = slot;

    // Linear Probing across open addressing buckets
    while (strcmp(dt->table[slot].entry_hash, "") != 0) {
        if (strcmp(dt->table[slot].entry_hash, text_hash) == 0) {
            return dt->table[slot].mapped_document_id; // Collision Match (Duplicate detected)
        }
        slot = (slot + 1) % VAULT_CAPACITY;
        if (slot == initial_slot) return -2; // Table completely full boundary warning
    }

    strncpy(dt->table[slot].entry_hash, text_hash, sizeof(dt->table[slot].entry_hash) - 1);
    dt->table[slot].mapped_document_id = doc_id;
    dt->element_count++;
    return -1; // New insertion completed successfully
}

void clear_table(DedupTable* dt) {
