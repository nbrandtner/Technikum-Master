CALL gds.kmeans.stream($graph, {
  nodeProperty: 'embedding',
  k: $k,
  randomSeed: $seed,
  initialSampler: 'kmeans++',
  numberOfRestarts: 1,
  maxIterations: 100,
  deltaThreshold: 0.00001,
  concurrency: 1
})
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).item_id AS id, communityId AS cluster
ORDER BY id
