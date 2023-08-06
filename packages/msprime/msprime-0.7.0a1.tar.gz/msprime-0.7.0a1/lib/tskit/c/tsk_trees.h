/**
 * @file tsk_trees.h
 * @brief Tskit core tree sequence operations.
 */
#ifndef TSK_TREES_H
#define TSK_TREES_H

#ifdef __cplusplus
extern "C" {
#endif

#include "tsk_tables.h"


#define TSK_SAMPLE_COUNTS  (1 << 0)
#define TSK_SAMPLE_LISTS   (1 << 1)

#define TSK_DIR_FORWARD 1
#define TSK_DIR_REVERSE -1


/**
@brief The tree sequence object.
*/
typedef struct {
    size_t num_trees;
    size_t num_samples;
    tsk_id_t *samples;
    /* If a node is a sample, map to its index in the samples list */
    tsk_id_t *sample_index_map;
    /* Map individuals to the list of nodes that reference them */
    tsk_id_t *individual_nodes_mem;
    tsk_id_t **individual_nodes;
    tsk_tbl_size_t *individual_nodes_length;
    /* For each tree, a list of sites on that tree */
    tsk_site_t *tree_sites_mem;
    tsk_site_t **tree_sites;
    tsk_tbl_size_t *tree_sites_length;
    /* For each site, a list of mutations at that site */
    tsk_mutation_t *site_mutations_mem;
    tsk_mutation_t **site_mutations;
    tsk_tbl_size_t *site_mutations_length;
    /* The underlying tables */
    tsk_tbl_collection_t *tables;
} tsk_treeseq_t;

typedef struct {
    tsk_treeseq_t *tree_sequence;
    size_t num_nodes;
    int flags;
    tsk_id_t *samples;
    /* The left-most root in the forest. Roots are sibs and all roots are found
     * via left_sib and right_sib */
    tsk_id_t left_root;
    /* Left and right physical coordinates of the tree */
    double left;
    double right;
    tsk_id_t *parent;          /* parent of node u */
    tsk_id_t *left_child;      /* leftmost child of node u */
    tsk_id_t *right_child;     /* rightmost child of node u */
    tsk_id_t *left_sib;        /* sibling to right of node u */
    tsk_id_t *right_sib;       /* sibling to the left of node u */
    bool *above_sample;
    size_t index;
    /* These are involved in the optional sample tracking; num_samples counts
     * all samples below a give node, and num_tracked_samples counts those
     * from a specific subset. */
    tsk_id_t *num_samples;
    tsk_id_t *num_tracked_samples;
    /* All nodes that are marked during a particular transition are marked
     * with a given value. */
    uint8_t *marked;
    uint8_t mark;
    /* These are for the optional sample list tracking. */
    tsk_id_t *left_sample;
    tsk_id_t *right_sample;
    tsk_id_t *next_sample;
    tsk_id_t *sample_index_map;
    /* traversal stacks */
    tsk_id_t *stack1;
    tsk_id_t *stack2;
    /* The sites on this tree */
    tsk_site_t *sites;
    tsk_tbl_size_t sites_length;
    /* Counters needed for next() and prev() transformations. */
    int direction;
    tsk_id_t left_index;
    tsk_id_t right_index;
} tsk_tree_t;

/* Diff iterator. TODO Not sure if we want to keep this, as it's not used
 * very much in the C code. */
typedef struct _tsk_edge_list_t {
    tsk_edge_t edge;
    struct _tsk_edge_list_t *next;
} tsk_edge_list_t;

typedef struct {
    size_t num_nodes;
    size_t num_edges;
    double tree_left;
    tsk_treeseq_t *tree_sequence;
    size_t insertion_index;
    size_t removal_index;
    size_t tree_index;
    tsk_edge_list_t *edge_list_nodes;
} tsk_diff_iter_t;

/****************************************************************************/
/* Tree sequence.*/
/****************************************************************************/

/**
@brief Allocate a new tree sequence from a table collection.

@rst
A tree sequence is a read-only view of a table collection with extra
structures that facilitate efficient tree iteratation and other operations.
@endrst

@param self A pointer to an uninitialised tsk_treeseq_t object.
@param tables A pointer to a tsk_tbl_collection_t object.
@param flags Allocation time options.
@return Return 0 on success or a negative value on failure.
*/
int tsk_treeseq_alloc(tsk_treeseq_t *self, tsk_tbl_collection_t *tables, int flags);

/**
@brief Load a tree sequence from file.

@rst
Reads a tree sequence from the specified file.
@endrst

@param self A pointer to an uninitialised tsk_treeseq_t object.
@param filename A NULL terminated string containing the filename.
@param flags Load time options. Currently unused.
@return Return 0 on success or a negative value on failure.
*/
int tsk_treeseq_load(tsk_treeseq_t *self, const char *filename, int flags);

int tsk_treeseq_dump(tsk_treeseq_t *self, const char *filename, int flags);
int tsk_treeseq_copy_tables(tsk_treeseq_t *self, tsk_tbl_collection_t *tables);
int tsk_treeseq_free(tsk_treeseq_t *self);
void tsk_treeseq_print_state(tsk_treeseq_t *self, FILE *out);

size_t tsk_treeseq_get_num_nodes(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_edges(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_migrations(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_sites(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_mutations(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_provenances(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_populations(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_individuals(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_trees(tsk_treeseq_t *self);
size_t tsk_treeseq_get_num_samples(tsk_treeseq_t *self);
char * tsk_treeseq_get_file_uuid(tsk_treeseq_t *self);
double tsk_treeseq_get_sequence_length(tsk_treeseq_t *self);
bool tsk_treeseq_is_sample(tsk_treeseq_t *self, tsk_id_t u);

int tsk_treeseq_get_node(tsk_treeseq_t *self, size_t index, tsk_node_t *node);
int tsk_treeseq_get_edge(tsk_treeseq_t *self, size_t index, tsk_edge_t *edge);
int tsk_treeseq_get_migration(tsk_treeseq_t *self, size_t index,
        tsk_migration_t *migration);
int tsk_treeseq_get_site(tsk_treeseq_t *self, size_t index, tsk_site_t *site);
int tsk_treeseq_get_mutation(tsk_treeseq_t *self, size_t index,
        tsk_mutation_t *mutation);
int tsk_treeseq_get_provenance(tsk_treeseq_t *self, size_t index,
        tsk_provenance_t *provenance);
int tsk_treeseq_get_population(tsk_treeseq_t *self, size_t index,
        tsk_population_t *population);
int tsk_treeseq_get_individual(tsk_treeseq_t *self, size_t index,
        tsk_individual_t *individual);
int tsk_treeseq_get_samples(tsk_treeseq_t *self, tsk_id_t **samples);
int tsk_treeseq_get_sample_index_map(tsk_treeseq_t *self,
        tsk_id_t **sample_index_map);

int tsk_treeseq_simplify(tsk_treeseq_t *self, tsk_id_t *samples,
        size_t num_samples, int flags, tsk_treeseq_t *output,
        tsk_id_t *node_map);
/* TODO do these belong in trees or stats? They should probably be in stats.
 * Keep them here for now until we figure out the correct interface.
 */
int tsk_treeseq_get_pairwise_diversity(tsk_treeseq_t *self,
    tsk_id_t *samples, size_t num_samples, double *pi);
int tsk_treeseq_genealogical_nearest_neighbours(tsk_treeseq_t *self,
        tsk_id_t *focal, size_t num_focal,
        tsk_id_t **reference_sets, size_t *reference_set_size, size_t num_reference_sets,
        int flags, double *ret_array);
int tsk_treeseq_mean_descendants(tsk_treeseq_t *self,
        tsk_id_t **reference_sets, size_t *reference_set_size, size_t num_reference_sets,
        int flags, double *ret_array);


/****************************************************************************/
/* Tree */
/****************************************************************************/

int tsk_tree_alloc(tsk_tree_t *self, tsk_treeseq_t *tree_sequence,
        int flags);
int tsk_tree_free(tsk_tree_t *self);
bool tsk_tree_has_sample_lists(tsk_tree_t *self);
bool tsk_tree_has_sample_counts(tsk_tree_t *self);
int tsk_tree_copy(tsk_tree_t *self, tsk_tree_t *source);
int tsk_tree_equal(tsk_tree_t *self, tsk_tree_t *other);
int tsk_tree_set_tracked_samples(tsk_tree_t *self,
        size_t num_tracked_samples, tsk_id_t *tracked_samples);
int tsk_tree_set_tracked_samples_from_sample_list(tsk_tree_t *self,
        tsk_tree_t *other, tsk_id_t node);
int tsk_tree_get_root(tsk_tree_t *self, tsk_id_t *root);
bool tsk_tree_is_sample(tsk_tree_t *self, tsk_id_t u);
size_t tsk_tree_get_num_roots(tsk_tree_t *self);
int tsk_tree_get_parent(tsk_tree_t *self, tsk_id_t u, tsk_id_t *parent);
int tsk_tree_get_time(tsk_tree_t *self, tsk_id_t u, double *t);
int tsk_tree_get_mrca(tsk_tree_t *self, tsk_id_t u, tsk_id_t v, tsk_id_t *mrca);
int tsk_tree_get_num_samples(tsk_tree_t *self, tsk_id_t u, size_t *num_samples);
int tsk_tree_get_num_tracked_samples(tsk_tree_t *self, tsk_id_t u,
        size_t *num_tracked_samples);
int tsk_tree_get_sites(tsk_tree_t *self, tsk_site_t **sites, tsk_tbl_size_t *sites_length);

void tsk_tree_print_state(tsk_tree_t *self, FILE *out);
/* Method for positioning the tree in the sequence. */
int tsk_tree_first(tsk_tree_t *self);
int tsk_tree_last(tsk_tree_t *self);
int tsk_tree_next(tsk_tree_t *self);
int tsk_tree_prev(tsk_tree_t *self);

/****************************************************************************/
/* Diff iterator */
/****************************************************************************/

int tsk_diff_iter_alloc(tsk_diff_iter_t *self, tsk_treeseq_t *tree_sequence);
int tsk_diff_iter_free(tsk_diff_iter_t *self);
int tsk_diff_iter_next(tsk_diff_iter_t *self,
        double *left, double *right,
        tsk_edge_list_t **edges_out, tsk_edge_list_t **edges_in);
void tsk_diff_iter_print_state(tsk_diff_iter_t *self, FILE *out);

#ifdef __cplusplus
}
#endif
#endif
