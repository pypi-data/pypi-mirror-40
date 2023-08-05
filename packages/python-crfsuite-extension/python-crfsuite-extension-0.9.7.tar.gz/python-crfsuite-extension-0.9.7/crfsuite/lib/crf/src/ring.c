/*
 * Implementation of curcular buffer.
 *
 * Copyright (c) 2015, Uladzimir Sidarenka
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the names of the authors nor the names of its contributors
 *       may be used to endorse or promote products derived from this
 *       software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
 * OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/* $Id$ */

///////////////
// Libraries //
///////////////
#include "ring.h"

#include <stdio.h>
#include <stdlib.h>

/////////////
// Methods //
/////////////
/* Set pointers in chain links forming the ring. */
static void crfsuite_chain_link_init(crfsuite_chain_link_t *a_chains, const size_t a_num)
{
  const size_t end = a_num > 0 ? a_num - 1: a_num;

  /* populate all elements except the last one */
  for (size_t i = 0; i < end; ++i) {
    a_chains[i].next = &a_chains[i + 1];
    a_chains[i + 1].prev = &a_chains[i];
  }
  /* populate last element provided that it exists */
  if (a_num > 0) {
    a_chains[end].next = &a_chains[0];
    a_chains[0].prev = &a_chains[end];
  }
}

/* Add an element to the ring. */
static void crfsuite_ring_push(crfsuite_ring_t *a_ring, int a_el)
{
  if (a_ring->max_items == 0)
    return;

  /* store new element in the last chain link of the ring */
  a_ring->tail->data = a_el;
  a_ring->tail = a_ring->tail->next;

  /* check if we exhuasted maximal capacity of the ring, and move head
     pointer if we did */
  if (a_ring->num_items == a_ring->max_items)
    a_ring->head = a_ring->head->next;
  else
    ++a_ring->num_items;
}

/* Remove last element from ring. */
static void crfsuite_ring_pop(crfsuite_ring_t *a_ring)
{
  /* if there is nothing to pop, return */
  if (a_ring->num_items == 0)
    return;

  /* set tail to previous element and decrement instance counter */
    a_ring->tail = a_ring->tail->prev;
  --a_ring->num_items;
}

// Reset counters of elements.
static void crfsuite_ring_reset(crfsuite_ring_t *a_ring)
{
  a_ring->num_items = 0;
  a_ring->head = a_ring->tail = (crfsuite_chain_link_t *) a_ring->internal;
}

// Clear ring and reset pointers.
static void crfsuite_ring_free(crfsuite_ring_t *a_ring)
{
  free(a_ring->internal);
  a_ring->max_items = a_ring->num_items = 0;
  a_ring->head = a_ring->tail = a_ring->internal = NULL;
}

int crfsuite_ring_create_instance(crfsuite_ring_t **a_ring, const size_t a_size)
{
  crfsuite_ring_t* iring = (crfsuite_ring_t*) calloc(1, sizeof(crfsuite_ring_t));

  if (iring != NULL) {
    iring->internal = (void *) calloc(a_size, sizeof(crfsuite_chain_link_t));
    if (iring->internal == NULL)
      return 1;

    iring->num_items = 0;
    iring->max_items = a_size;
    iring->head = iring->tail = (crfsuite_chain_link_t *) iring->internal;
    crfsuite_chain_link_init(iring->head, iring->max_items);

    iring->push = crfsuite_ring_push;
    iring->pop = crfsuite_ring_pop;
    iring->reset = crfsuite_ring_reset;
    iring->free = crfsuite_ring_free;

    *a_ring = (void *) iring;
    return 0;
  } else {
    return -1;
  }
}
