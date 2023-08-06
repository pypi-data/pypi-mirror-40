# Container Tree

This is a library that demonstrates different methods to build container trees. 
Across different kinds of trees, we generate a [Trie](https://en.wikipedia.org/wiki/Trie) 
to represent a file or container hierarchy. We can either generate 
[trees](https://singularityhub.github.io/container-tree/examples/files_tree/demo/), 
or [comparison matrices](https://singularityhub.github.io/container-tree/examples/heatmap/demo/) 
using them!

# Container Trees

## What is a container tree?

In the context of containers, a container tree will map the file system of
a container into a tree structure. This means that each node represents
a file path, and holds with it metadata like counts and tags. And yes! This
means that for a single Container Tree, you can map multiple containers to it,
and have the nodes tagged with the containers that are represented there.
For example, we might have this node:

```
Node
  name: /usr/local/bin
  count: 2
  tags: ["ubuntu", "centos"]
```

This would say that there are two containers mapped to the tree, ubuntu and
centos, and both of them have the path /usr/local/bin. We can then calculate
similarity metrics by walking the tree and comparing containers defined at each
node. Intuitively, the root node of the tree is the root of a filesystem /.

## What is a container package tree?

In the case that we want to organize our tree based on packages and versions,
we can use the container package tree. Specifically, we are interested in 
pip (python) and apt (debian/ubuntu). Each node of this tree represents one
level of a package, and to the node we map containers that have the package
at that level. For example, we might have these levels for the pip tree:

```
Pip
   ___ requests
               ___ requests == 2.0
               ___ requests == 2.1
               ___ requests == 2.2
               ...
```

Each node above is a particular version of requests, and we map containers to it
that have that version. Here is the node for requests == 2.2:

```
Node:
  name: requests == 2.2
  count: 2
  tags ["ubuntu", "centos"]
```

This means that we can very easily compare containers by doing a single walk
of the tree. It also means that we can identify the last common ancestor
for any given package to determine similarity. For example, if two containers
had different versions of requests, they would be similar up to the level
of the Node for just "requests."

## What is a collection tree?

If you want to move up one level and think about container inheritance (meaning
the FROM statement in the Dockerfile recipes) you might be interested in a
Collection tree. In a collection tree, each Node represents a container base,
and the count is the number of times we find it for some container set that 
we have parsed. For this kind of tree, the root node is the scratch base image.

## Install

```python
pip install containertree
```
```
git clone https://www.github.com/singularityhub/container.tree
cd container.tree
python setup.py install
```

# Classes

## ContainerTreeBase

The `ContainerTreeBase` class is a base class that can read in general lists,
json, http, or other input data. The function to generate the tree, `_make_tree`,
is not defined and must be implemented by the subclass. 
If you want to create a subclass, you can define any additional parsing needed 
for your input under a function called `_load`. It should check that `self.data` 
is not None, and if not, expect it to be loaded json from the input. 
You can continue parsing it and save again the final result to `self.data`. 
See `ContainerDiffTree` for an example.


## ContainerTree

The `ContainerTree` class is a subclass of `ContainerTreeBase` that expects
to build a file system tree to describe one or more containers. The json input
should have a list of dictionaries, each dictionary representing a complete 
filepath (e.g., `/etc/ssl`). The key "Name" is required in the dictionary to 
identify the file. This class might be suited for you if you have a custom


## ContainerDiffTree

This is a subclass of `ContainerTree`, specifically with an added `_load` function
to additionally parse the data loaded by the base ContainerTree class to support 
the data structure exported by container diff, which is a list with the expected
structure under "Analysis". For example:

```bash
[ {
  'Analysis': [
   ...
      {'Name': '/etc/ssl/certs/93bc0acc.0', 'Size': 1204},
      {'Name': '/etc/ssl/certs/9479c8c3.0', 'Size': 1017},
   ...],
  'AnalyzeType': 'File',
  'Image': '/tmp/tmp.qXbcpKCWxg/c2f46186d20ce41a1e1cad7b362ad9f6a5b679cd6535e865c4170cc93f4501a4.tar'}]
```

We are only interested in the list under "Analysis," and the kind of analysis
might be File, Apt, or Pip. It's unlikely that you'll instantiate a ContainerDiffTree,
but you might instantiate a ContainerFileTree or ContainerPipTree.

## Examples

### Create a Container File Tree

These examples are also provided in the [examples](examples) folder.
For this first example, we will be using the [Container API](https://singularityhub.github.io/api/) 
served by the Singularity Hub robots to read in lists of files.

```python
from containertree import ContainerFileTree
import requests

# Path to database of container-api 
database = "https://singularityhub.github.io/api/files"
containers = requests.get(database).json()
entry = containers[0]  

# Google Container Diff Analysis Type "File" Structure
tree = ContainerFileTree(entry['url'])

# To find a node based on path
tree.find('/etc/ssl')
# Node<ssl>

# Trace a path, returning all nodes
tree.trace('/etc/ssl')
# [Node<etc>, Node<ssl>]

# Insert a new node path
tree.insert('/etc/tomato')
tree.trace('/etc/tomato')
#[Node<etc>, Node<tomato>]

# Get count of a node
tree.get_count('/etc/tomato')
# 1
tree.insert('/etc/tomato')
tree.get_count('/etc/tomato')
# 2

# Update the tree with a second container!
new_entry = containers[1]  
tree.update(new_entry['url'])
```

### Add a URI

Let's say that we don't have a list of files, either local or via http. If
we have [container-diff](https://github.com/GoogleContainerTools/container-diff) installed, 
we can add containers to the tree based on unique resource identifier (URI).

```python
from containertree import ContainerFileTree

# Google Container Diff Analysis Type "File" Structure
tree = ContainerFileTree("vanessa/salad")

# Find a node directly
tree.find('/code/salad')
Node<salad>

# Search for names
tree.search('salad')
[Node<salad>, Node<salad>, Node<salad.go>]

# These are different salads!
for res in tree.search('salad'):
    print(res.name)

/code/salad
/go/src/github.com/vsoch/salad
/go/src/github.com/vsoch/salad/salad.go
```

### Add Containers

If you are adding more than one container to a tree, you should keep track of
the containers that are represented at each node (meaning the file/folder exists
in the container). You can do this by using node tags. Here is how to create
(and update a tree) using these tags!

```python
entry1 = containers[0]  
entry2 = containers[1]
tag1=entry1['collection']
#'54r4/sara-server-vre'
tag2=entry2['collection']
#'A33a/sjupyter'
tree = ContainerFileTree(entry1['url'], tag=tag1)

# What are the tags for the root node?
tree.root.tags
Out[18]: ['54r4/sara-server-vre']

# Update the container tree with the second container
tree.update(entry2['url'], tag=tag2)
# ['54r4/sara-server-vre', 'A33a/sjupyter']
```

You can imagine having a tagged Trie will be very useful for different algorithms
to traverse the tree and compare the entities defined at the different nodes!

### Create a Container Package Tree

You can also create trees to map different containers to packages maintained
under Pip and Apt.

```python
from containertree.tree import ContainerAptTree

# Initilize a tree with packages from a container
apt = ContainerAptTree('singularityhub/sregistry-cli')

apt.trace('wget')
# [Node<>, Node<wget>, Node<1.18-5 deb9u2>]
```
```python
from containertree.tree import ContainerPipTree

# Initilize a tree with packages from a container
pip = ContainerPipTree('neurovault/neurovault')

# How many nodes?
pip.count
175

pip.trace('nilearn')
# [Node<>, Node<nilearn>, Node<0.4.2>]
```
The idea would be to add containers to the tree with "update" and as you do,
tag the nodes with the container name (or other interesting metadata).

### Container Comparisons

Once we have added a second tree, we can traverse the trie to calculate comparisons!
The score represents the percentage of nodes defined in one or more containers (call
this total) that are represented in BOTH containers.

```python
# using the tree from above, where we have two tags
tags = tree.root.tags
# ['54r4/sara-server-vre', 'A33a/sjupyter']

# Calculate the similarity
scores = tree.similarity_score(tags)

# {'diff': 44185,
# 'same': 12201,
# 'score': 0.21638349945021815,
# 'tags': ['54r4/sara-server-vre', 'A33a/sjupyter'],
# 'total': 56386}
```

You can then use this to generate a heatmap / matrix of similarity scores, or anything
else you desire! For example, [here is the heatmap](https://singularityhub.github.io/container-tree/examples/heatmap/demo/) that I made.

What would we do next? Would we want to know what files change between versions of a container? If you want to do some sort of mini analysis with me, please reach out! I'd like to do this soon.

### Create a Collection Tree

We've recently added a new kind of tree, the collection tree! With a collection 
tree, each node is a container, and we build the tree based on FROM statements
in Dockerfiles (the bases). Since the image manifets don't give hints about FROM,
we must build this from Dockerfiles, OR from a URI and it's from URI (meaning
we can collect pairs of parents and children).

```python
from containertree import CollectionTree

# Initialize a collection tree
tree = CollectionTree()
tree.update('singularityhub/containertree', 'continuumio/miniconda3')

# tree.root.children
# [MultiNode<continuumio/miniconda3>]

tree.update('singularityhub/sregistry-cli', 'continuumio/miniconda3')
```

We've just added a second child to the parent `continuumio/miniconda3` (with
implied tag "latest")

```python
# tree.root.children[0].children

{'latest': [ MultiNode<singularityhub/containertree>,
             MultiNode<singularityhub/sregistry-cli> ] }
```

Now let's try updating with the same namespace container, but a different tag:

```python
tree.update('singularityhub/containertree', 'continuumio/miniconda3:1.0')

{'1.0': [MultiNode<singularityhub/containertree>],
 'latest': [MultiNode<singularityhub/sregistry-cli>]}
```

Since a container with a specific unique resource identifier can only have
one parent, this represents moving the node in the tree. The new parent tag is
1.0. 

The two tags are still under the same namespace, (continuumio/miniconda3), and 
organized by the tag. Thus, when you do find for a container, you can return the 
entire node with all tags:

```python
tree.find('continuumio/miniconda3')
MultiNode<continuumio/miniconda3>
```

We can also do this from a Dockerfile

```
# The parent is the same continuumio/miniconda3
tree.update('vanessa/salad', "Dockerfile")

tree.find('continuumio/miniconda3').children
{'1.0': [MultiNode<singularityhub/containertree>],
 'latest': [MultiNode<singularityhub/sregistry-cli>, MultiNode<vanessa/salad>]}
```

Now let's say we add the actual parent of continuumio/miniconda3 (it's not scratch),
but let's pretend it's the library/python base image.

```python
tree.update('continuumio/miniconda3', 'library/python')
```

We now see the new child in the parent node

```python
tree.root.children
[MultiNode<continuumio/miniconda3>, MultiNode<library/python>]
```

and node that continuumio/miniconda3 is still represented, but for a different
tag (not latest):

```python
tree.root.children[0].children
{'1.0': [MultiNode<singularityhub/containertree>]}
```

And the "latest" tag, previously under scratch, is now under library/python:

```python
tree.root.children[1].children
{'latest': [MultiNode<continuumio/miniconda3>]}
```

and it's inherited the previous children.

```python
tree.root.children[1].children['latest'][0].children
{'latest': [MultiNode<singularityhub/sregistry-cli>, MultiNode<vanessa/salad>]}
```

# Visualize

These are under development! Here are some quick examples:

![examples/heatmap/heatmap.png](examples/heatmap/heatmap.png)

## Demo

Generate an example file tree using the [containertree](https://cloud.docker.com/u/singularityhub/repository/docker/singularityhub/container-tree) Docker container.

```bash
$ docker run -it -p 9779:9779 singularityhub/container-tree demo
Selecting container from https://singularityhub.github.io/api/files...
Generating files tree!
ContainerTree<56386>
Webroot: /tmp/tmpizxgn5jk
Exporting data for d3 visualization
Serving at localhost:9779
```
Then open up your browser to [http://localhost:9779](http://localhost:9779).
The container is randomly selected from the Singularity Hub (static) API.

## Generate Tree from Docker URI

You can generate just static files. Notice that we are telling the container
to generate output in /data inside the container, which is mapped to 
an output folder we just created.

```bash
mkdir -p output
$ docker run -v $PWD/output:/data -it -p 9779:9779 singularityhub/container-tree generate vanessa/salad --output /data
```

Then you can see your output files, a data.json and index.html:

```bash
$ tree output
output/
├── data.json
└── index.html
```

You can start a temporary server to view the files:

```bash
cd output
python -m http.server 9999
# open localhost:9999
```

## Tree Templates

The templates provided are each web (html) files that expect a data.json tree.
To see available templates:

```bash
$ docker run singularityhub/container-tree templates
Templates:

collection_tree
treemap
similarity_scatter
heatmap
tree
heatmap-large
files_tree
container_tree
shub_tree
```

And then you can specify a template name with the `--template` argument to the
generate command. The default is a files tree.


#### Hierarchy

 - [General Tree](https://singularityhub.github.io/container-tree/examples/tree/demo/)
 - [Files Tree](https://singularityhub.github.io/container-tree/examples/files_tree/demo/)
 - [Shub Tree](https://singularityhub.github.io/container-tree/examples/shub_tree/demo/)


#### Comparison

 - [Heatmap](https://singularityhub.github.io/container-tree/examples/heatmap/demo/)

The examples and their generation are provided in each of the subfolders of the [examples](examples) directory.
