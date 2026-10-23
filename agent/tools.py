"""DSA Buddy tools: structured DSA content served to the Strands agent.

All data is defined inline (no external calls, no file I/O). The LLM reads each tool's
docstring to decide when to call it.
"""

from __future__ import annotations

from strands import tool

# ---------------------------------------------------------------------------
# Structured DSA knowledge base
# ---------------------------------------------------------------------------

DSA_TOPICS: dict[str, dict] = {
    "array": {
        "description": "A collection of elements stored at contiguous memory locations",
        "analogy": "Like a row of numbered lockers in a school hallway",
        "time_complexity": {"access": "O(1)", "search": "O(n)", "insert": "O(n)", "delete": "O(n)"},
        "space_complexity": "O(n)",
        "use_cases": ["Storing a list of students", "Image pixel storage", "Matrix operations"],
        "steps": [
            "1. Declare an array with a fixed size",
            "2. Access elements using index (0-based)",
            "3. Traverse by iterating from index 0 to n-1",
            "4. Insert by shifting elements right from insertion point",
            "5. Delete by shifting elements left from deletion point",
        ],
        "code": {
            "python": "arr = [1, 2, 3, 4, 5]\nprint(arr[0])  # Access: O(1)\nfor x in arr:  # Traverse: O(n)\n    print(x)",
            "c": "int arr[5] = {1, 2, 3, 4, 5};\nprintf(\"%d\", arr[0]);  // Access: O(1)",
            "cpp": "vector<int> arr = {1, 2, 3, 4, 5};\ncout << arr[0];  // Access: O(1)",
            "java": "int[] arr = {1, 2, 3, 4, 5};\nSystem.out.println(arr[0]);  // Access: O(1)",
        },
        "practice_problems": [
            {
                "title": "Find maximum element in array",
                "difficulty": "beginner",
                "hint1": "Initialize a variable with the first element as max",
                "hint2": "Compare each element with max and update if larger",
                "solution_approach": "Linear scan O(n): iterate once, tracking the maximum seen so far",
            },
            {
                "title": "Reverse an array in-place",
                "difficulty": "beginner",
                "hint1": "Use two pointers: one at start, one at end",
                "hint2": "Swap elements at both pointers, then move them toward each other",
                "solution_approach": "Two-pointer technique O(n): swap arr[left] and arr[right] while left < right",
            },
        ],
    },
    "linked_list": {
        "description": "A sequence of nodes where each node stores data and a pointer to the next node",
        "analogy": "Like a treasure hunt where each clue leads to the next location",
        "time_complexity": {"access": "O(n)", "search": "O(n)", "insert_head": "O(1)", "insert_tail": "O(n)", "delete": "O(n)"},
        "space_complexity": "O(n)",
        "use_cases": ["Implementing stacks and queues", "Browser history", "Music playlist"],
        "steps": [
            "1. Create a Node class with data and next pointer",
            "2. Head pointer points to first node; last node's next is None",
            "3. Traverse by following next pointers from head",
            "4. Insert at head: new_node.next = head; head = new_node",
            "5. Delete: find node before target, update its next pointer",
        ],
        "code": {
            "python": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n\n    def insert_head(self, data):\n        new_node = Node(data)\n        new_node.next = self.head\n        self.head = new_node",
            "c": "struct Node {\n    int data;\n    struct Node* next;\n};\n\nstruct Node* insert_head(struct Node* head, int data) {\n    struct Node* new_node = malloc(sizeof(struct Node));\n    new_node->data = data;\n    new_node->next = head;\n    return new_node;\n}",
            "cpp": "struct Node {\n    int data;\n    Node* next;\n    Node(int d) : data(d), next(nullptr) {}\n};\n\nvoid insert_head(Node*& head, int data) {\n    Node* new_node = new Node(data);\n    new_node->next = head;\n    head = new_node;\n}",
            "java": "class Node {\n    int data;\n    Node next;\n    Node(int data) { this.data = data; this.next = null; }\n}\n\nclass LinkedList {\n    Node head;\n    void insertHead(int data) {\n        Node newNode = new Node(data);\n        newNode.next = head;\n        head = newNode;\n    }\n}",
        },
        "practice_problems": [
            {
                "title": "Find the length of a linked list",
                "difficulty": "beginner",
                "hint1": "Traverse the list counting each node",
                "hint2": "Use a counter variable, increment for each node until next is None",
                "solution_approach": "Traverse once O(n): count nodes until you reach None",
            },
            {
                "title": "Detect a cycle in a linked list",
                "difficulty": "intermediate",
                "hint1": "What if two pointers move at different speeds?",
                "hint2": "Use Floyd's algorithm: slow pointer moves 1 step, fast pointer moves 2 steps",
                "solution_approach": "Floyd's cycle detection O(n) time O(1) space: if fast and slow meet, cycle exists",
            },
        ],
    },
    "stack": {
        "description": "A LIFO (Last In First Out) data structure",
        "analogy": "Like a stack of plates — you always take from the top",
        "time_complexity": {"push": "O(1)", "pop": "O(1)", "peek": "O(1)"},
        "space_complexity": "O(n)",
        "use_cases": ["Function call stack", "Undo/redo in editors", "Expression evaluation", "Browser back button"],
        "steps": [
            "1. Initialize empty stack",
            "2. PUSH: add element to top",
            "3. POP: remove element from top",
            "4. PEEK: view top without removing",
            "5. Check isEmpty before popping",
        ],
        "code": {
            "python": "stack = []\nstack.append(1)  # push\nstack.append(2)\ntop = stack.pop()  # pop: returns 2\npeek = stack[-1]  # peek: returns 1",
            "c": "#define MAX 100\nint stack[MAX], top = -1;\nvoid push(int x) { stack[++top] = x; }\nint pop() { return stack[top--]; }\nint peek() { return stack[top]; }",
            "cpp": "#include <stack>\nstack<int> s;\ns.push(1); s.push(2);\nint top = s.top(); s.pop();  // top=2, then removed",
            "java": "import java.util.Stack;\nStack<Integer> s = new Stack<>();\ns.push(1); s.push(2);\nint top = s.pop();  // returns 2",
        },
        "practice_problems": [
            {
                "title": "Check for balanced parentheses",
                "difficulty": "beginner",
                "hint1": "Push opening brackets, pop when you see closing brackets",
                "hint2": "Check if the popped bracket matches the closing bracket type",
                "solution_approach": "Use stack: push '(' '[' '{', on closing check if top matches, return stack empty at end",
            },
        ],
    },
    "queue": {
        "description": "A FIFO (First In First Out) data structure",
        "analogy": "Like a queue at a bus stop — first person in line boards first",
        "time_complexity": {"enqueue": "O(1)", "dequeue": "O(1)"},
        "space_complexity": "O(n)",
        "use_cases": ["Print spooler", "BFS graph traversal", "Task scheduling", "CPU scheduling"],
        "steps": [
            "1. Initialize empty queue",
            "2. ENQUEUE: add to rear",
            "3. DEQUEUE: remove from front",
            "4. FRONT: peek at front without removing",
            "5. Check isEmpty before dequeuing",
        ],
        "code": {
            "python": "from collections import deque\nq = deque()\nq.append(1)  # enqueue\nq.append(2)\nfront = q.popleft()  # dequeue: returns 1",
            "c": "#define MAX 100\nint queue[MAX], front = 0, rear = 0;\nvoid enqueue(int x) { queue[rear++] = x; }\nint dequeue() { return queue[front++]; }",
            "cpp": "#include <queue>\nqueue<int> q;\nq.push(1); q.push(2);\nint front = q.front(); q.pop();  // front=1, then removed",
            "java": "import java.util.LinkedList;\nQueue<Integer> q = new LinkedList<>();\nq.offer(1); q.offer(2);\nint front = q.poll();  // returns 1",
        },
        "practice_problems": [
            {
                "title": "Implement a queue using two stacks",
                "difficulty": "intermediate",
                "hint1": "Use stack1 for enqueue, stack2 for dequeue",
                "hint2": "When dequeuing, if stack2 is empty, pop all elements from stack1 into stack2",
                "solution_approach": "Amortized O(1) per operation: lazy transfer between stacks",
            },
        ],
    },
    "binary_search": {
        "description": "An efficient algorithm to find an element in a SORTED array by halving the search space",
        "analogy": "Like finding a word in a dictionary — open the middle, decide which half to search",
        "time_complexity": {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)"},
        "space_complexity": "O(1) iterative, O(log n) recursive",
        "use_cases": ["Searching in sorted arrays", "Finding insertion point", "Answering yes/no questions on monotone functions"],
        "steps": [
            "1. Set left=0, right=len(arr)-1",
            "2. While left <= right: compute mid = (left+right)//2",
            "3. If arr[mid] == target: found! return mid",
            "4. If arr[mid] < target: search right half: left = mid+1",
            "5. If arr[mid] > target: search left half: right = mid-1",
            "6. If loop ends without finding: return -1",
        ],
        "code": {
            "python": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\n# Test: arr=[1,3,5,7,9], target=7 -> returns 3",
            "c": "int binary_search(int arr[], int n, int target) {\n    int left = 0, right = n - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        else if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
            "cpp": "int binarySearch(vector<int>& arr, int target) {\n    int left = 0, right = arr.size() - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        else if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
            "java": "int binarySearch(int[] arr, int target) {\n    int left = 0, right = arr.length - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        else if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
        },
        "practice_problems": [
            {
                "title": "Find the first occurrence of a target in sorted array",
                "difficulty": "intermediate",
                "hint1": "Binary search finds one occurrence; how to ensure it's the first?",
                "hint2": "When you find the target, don't stop — continue searching left half",
                "solution_approach": "Modified binary search: on match, save index and set right = mid-1 to keep searching left",
            },
            {
                "title": "Find square root without using sqrt()",
                "difficulty": "intermediate",
                "hint1": "Think of it as finding an integer x where x*x <= n < (x+1)*(x+1)",
                "hint2": "Binary search on the answer space [0, n]",
                "solution_approach": "Binary search O(log n): if mid*mid == n return mid, if < n search right, else search left",
            },
        ],
    },
    "bubble_sort": {
        "description": "A simple sorting algorithm that repeatedly swaps adjacent elements if they are in wrong order",
        "analogy": "Like bubbles rising to the surface — larger elements bubble up to the end each pass",
        "time_complexity": {"best": "O(n)", "average": "O(n^2)", "worst": "O(n^2)"},
        "space_complexity": "O(1)",
        "use_cases": ["Educational purposes", "Small datasets", "Nearly sorted arrays with optimization"],
        "steps": [
            "1. Outer loop: pass number (0 to n-1)",
            "2. Inner loop: compare adjacent elements arr[j] and arr[j+1]",
            "3. If arr[j] > arr[j+1]: swap them",
            "4. After each pass, the largest unsorted element is in its correct position",
            "5. Optimization: if no swaps in a pass, array is already sorted — break early",
        ],
        "code": {
            "python": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped:\n            break  # already sorted\n    return arr",
            "c": "void bubble_sort(int arr[], int n) {\n    for (int i = 0; i < n - 1; i++) {\n        int swapped = 0;\n        for (int j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j+1]) {\n                int tmp = arr[j]; arr[j] = arr[j+1]; arr[j+1] = tmp;\n                swapped = 1;\n            }\n        }\n        if (!swapped) break;\n    }\n}",
            "cpp": "void bubbleSort(vector<int>& arr) {\n    int n = arr.size();\n    for (int i = 0; i < n - 1; i++) {\n        bool swapped = false;\n        for (int j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                swap(arr[j], arr[j + 1]);\n                swapped = true;\n            }\n        }\n        if (!swapped) break;\n    }\n}",
            "java": "void bubbleSort(int[] arr) {\n    int n = arr.length;\n    for (int i = 0; i < n - 1; i++) {\n        boolean swapped = false;\n        for (int j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                int tmp = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = tmp;\n                swapped = true;\n            }\n        }\n        if (!swapped) break;\n    }\n}",
        },
        "practice_problems": [
            {
                "title": "Count the number of swaps in bubble sort",
                "difficulty": "beginner",
                "hint1": "Add a counter inside the swap block",
                "hint2": "Increment counter each time you do a swap",
                "solution_approach": "Modify bubble sort to count swaps; return the count alongside sorted array",
            },
        ],
    },
    "merge_sort": {
        "description": "A divide-and-conquer sorting algorithm that recursively splits, sorts, and merges",
        "analogy": "Like sorting playing cards by splitting the deck into halves, sorting each half, then merging",
        "time_complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)"},
        "space_complexity": "O(n)",
        "use_cases": ["Large datasets", "Linked list sorting", "External sorting", "Stable sort needed"],
        "steps": [
            "1. BASE CASE: if array has 0 or 1 element, it's already sorted",
            "2. DIVIDE: split array in half at mid = len//2",
            "3. CONQUER: recursively sort left half and right half",
            "4. MERGE: merge two sorted halves into one sorted array",
            "5. Merge: compare front elements of both halves, take the smaller one",
        ],
        "code": {
            "python": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i]); i += 1\n        else:\n            result.append(right[j]); j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result",
            "c": "void merge(int arr[], int l, int m, int r) {\n    int n1 = m-l+1, n2 = r-m;\n    int L[n1], R[n2];\n    for (int i=0;i<n1;i++) L[i]=arr[l+i];\n    for (int j=0;j<n2;j++) R[j]=arr[m+1+j];\n    int i=0,j=0,k=l;\n    while(i<n1&&j<n2) arr[k++]=(L[i]<=R[j])?L[i++]:R[j++];\n    while(i<n1) arr[k++]=L[i++];\n    while(j<n2) arr[k++]=R[j++];\n}\nvoid merge_sort(int arr[],int l,int r){if(l<r){int m=(l+r)/2;merge_sort(arr,l,m);merge_sort(arr,m+1,r);merge(arr,l,m,r);}}",
            "cpp": "void mergeSort(vector<int>& arr, int l, int r) {\n    if (l >= r) return;\n    int m = l + (r - l) / 2;\n    mergeSort(arr, l, m);\n    mergeSort(arr, m + 1, r);\n    // merge arr[l..m] and arr[m+1..r] in place\n}",
            "java": "void mergeSort(int[] arr, int l, int r) {\n    if (l < r) {\n        int m = (l + r) / 2;\n        mergeSort(arr, l, m);\n        mergeSort(arr, m + 1, r);\n        merge(arr, l, m, r);\n    }\n}",
        },
        "practice_problems": [
            {
                "title": "Merge two sorted arrays into one sorted array",
                "difficulty": "beginner",
                "hint1": "Use two pointers, one for each array",
                "hint2": "Compare current elements, add the smaller one to result, advance that pointer",
                "solution_approach": "Two-pointer merge O(n+m): compare and pick smaller, then append remaining elements",
            },
        ],
    },
    "quick_sort": {
        "description": "A divide-and-conquer sorting algorithm that partitions around a pivot element",
        "analogy": "Like organizing books by picking one book as reference and putting cheaper ones left, expensive ones right",
        "time_complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n^2)"},
        "space_complexity": "O(log n) average",
        "use_cases": ["General purpose sorting", "In-place sorting", "Cache-friendly sorting"],
        "steps": [
            "1. Choose a pivot (last element is common choice)",
            "2. PARTITION: rearrange so elements < pivot are left, > pivot are right",
            "3. Pivot is now in its final sorted position",
            "4. Recursively quicksort the left subarray",
            "5. Recursively quicksort the right subarray",
        ],
        "code": {
            "python": "def quick_sort(arr, low, high):\n    if low < high:\n        pi = partition(arr, low, high)\n        quick_sort(arr, low, pi - 1)\n        quick_sort(arr, pi + 1, high)\n\ndef partition(arr, low, high):\n    pivot = arr[high]\n    i = low - 1\n    for j in range(low, high):\n        if arr[j] <= pivot:\n            i += 1\n            arr[i], arr[j] = arr[j], arr[i]\n    arr[i + 1], arr[high] = arr[high], arr[i + 1]\n    return i + 1",
            "c": "int partition(int arr[], int low, int high) {\n    int pivot = arr[high], i = low - 1;\n    for (int j = low; j < high; j++)\n        if (arr[j] <= pivot) { i++; int t=arr[i]; arr[i]=arr[j]; arr[j]=t; }\n    int t=arr[i+1]; arr[i+1]=arr[high]; arr[high]=t;\n    return i + 1;\n}\nvoid quick_sort(int arr[], int low, int high) {\n    if (low < high) { int pi=partition(arr,low,high); quick_sort(arr,low,pi-1); quick_sort(arr,pi+1,high); }\n}",
            "cpp": "int partition(vector<int>& arr, int low, int high) {\n    int pivot = arr[high], i = low - 1;\n    for (int j = low; j < high; j++)\n        if (arr[j] <= pivot) swap(arr[++i], arr[j]);\n    swap(arr[i + 1], arr[high]);\n    return i + 1;\n}",
            "java": "int partition(int[] arr, int low, int high) {\n    int pivot = arr[high], i = low - 1;\n    for (int j = low; j < high; j++)\n        if (arr[j] <= pivot) { int t=arr[++i]; arr[i]=arr[j]; arr[j]=t; }\n    int t=arr[i+1]; arr[i+1]=arr[high]; arr[high]=t;\n    return i + 1;\n}",
        },
        "practice_problems": [
            {
                "title": "Find the k-th smallest element using QuickSelect",
                "difficulty": "advanced",
                "hint1": "QuickSelect uses the same partition as QuickSort",
                "hint2": "After partition, if pivot index == k-1, you found it; else recurse on one side only",
                "solution_approach": "QuickSelect O(n) average: partition and recurse only on the side containing k",
            },
        ],
    },
    "recursion": {
        "description": "A technique where a function calls itself to solve a smaller version of the same problem",
        "analogy": "Like looking up a word in a dictionary that says 'see: word' — but with a base case to stop",
        "time_complexity": {"varies": "Depends on number of recursive calls and work per call"},
        "space_complexity": "O(depth) for call stack",
        "use_cases": ["Tree traversal", "Divide and conquer", "Backtracking", "Mathematical sequences"],
        "steps": [
            "1. Identify the BASE CASE: the simplest input that can be solved directly",
            "2. Identify the RECURSIVE CASE: how to reduce problem to a smaller version",
            "3. Trust the recursion: assume the recursive call works correctly",
            "4. Combine: how to build the answer from the recursive result",
            "5. Check: does every path reach the base case?",
        ],
        "code": {
            "python": "def factorial(n):\n    # Base case: 0! = 1\n    if n == 0:\n        return 1\n    # Recursive case: n! = n * (n-1)!\n    return n * factorial(n - 1)\n\n# factorial(5) -> 5 * factorial(4) -> ... -> 5*4*3*2*1 = 120",
            "c": "int factorial(int n) {\n    if (n == 0) return 1;  // base case\n    return n * factorial(n - 1);  // recursive case\n}",
            "cpp": "int factorial(int n) {\n    if (n == 0) return 1;\n    return n * factorial(n - 1);\n}",
            "java": "int factorial(int n) {\n    if (n == 0) return 1;\n    return n * factorial(n - 1);\n}",
        },
        "practice_problems": [
            {
                "title": "Calculate nth Fibonacci number using recursion",
                "difficulty": "beginner",
                "hint1": "F(n) = F(n-1) + F(n-2); base cases are F(0)=0 and F(1)=1",
                "hint2": "Write the base cases first, then the recursive case",
                "solution_approach": "Direct recursion O(2^n) naive; note memoization makes it O(n) — discuss trade-off",
            },
        ],
    },
    "tree": {
        "description": "A hierarchical data structure with a root node and subtrees of children",
        "analogy": "Like a family tree — one ancestor at top, children branching down",
        "time_complexity": {"search_bst": "O(log n) average", "insert_bst": "O(log n) average", "traversal": "O(n)"},
        "space_complexity": "O(n)",
        "use_cases": ["File system structure", "HTML DOM", "Database indexing", "Decision trees"],
        "steps": [
            "1. A node has: data, left child pointer, right child pointer",
            "2. BST property: left subtree values < root < right subtree values",
            "3. Inorder traversal (left, root, right) gives sorted order for BST",
            "4. Insert: compare with root, go left or right, insert at null position",
            "5. Search: compare with root, go left if smaller, right if larger",
        ],
        "code": {
            "python": "class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n\ndef insert(root, val):\n    if not root:\n        return TreeNode(val)\n    if val < root.val:\n        root.left = insert(root.left, val)\n    else:\n        root.right = insert(root.right, val)\n    return root\n\ndef inorder(root):\n    if root:\n        inorder(root.left); print(root.val); inorder(root.right)",
            "c": "struct TreeNode { int val; struct TreeNode *left, *right; };\nstruct TreeNode* insert(struct TreeNode* root, int val) {\n    if (!root) { struct TreeNode* n=malloc(sizeof(*n)); n->val=val; n->left=n->right=NULL; return n; }\n    if (val < root->val) root->left = insert(root->left, val);\n    else root->right = insert(root->right, val);\n    return root;\n}",
            "cpp": "struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v):val(v),left(nullptr),right(nullptr){} };\nTreeNode* insert(TreeNode* root, int val) {\n    if (!root) return new TreeNode(val);\n    if (val < root->val) root->left = insert(root->left, val);\n    else root->right = insert(root->right, val);\n    return root;\n}",
            "java": "class TreeNode { int val; TreeNode left, right; TreeNode(int v){val=v;} }\nTreeNode insert(TreeNode root, int val) {\n    if (root == null) return new TreeNode(val);\n    if (val < root.val) root.left = insert(root.left, val);\n    else root.right = insert(root.right, val);\n    return root;\n}",
        },
        "practice_problems": [
            {
                "title": "Find the height of a binary tree",
                "difficulty": "beginner",
                "hint1": "The height is 1 + maximum of left and right subtree heights",
                "hint2": "Base case: height of null tree is 0 (or -1 depending on definition)",
                "solution_approach": "Recursive O(n): height(root) = 1 + max(height(left), height(right))",
            },
        ],
    },
    "graph": {
        "description": "A collection of nodes (vertices) connected by edges",
        "analogy": "Like a map of cities connected by roads",
        "time_complexity": {"BFS": "O(V+E)", "DFS": "O(V+E)"},
        "space_complexity": "O(V+E)",
        "use_cases": ["Social networks", "GPS navigation", "Web crawling", "Dependency resolution"],
        "steps": [
            "1. Represent graph as adjacency list (dict of lists) or matrix",
            "2. BFS: use a queue, visit level by level, mark visited",
            "3. DFS: use a stack (or recursion), go deep first, mark visited",
            "4. Always mark nodes visited to avoid infinite loops in cyclic graphs",
            "5. BFS finds shortest path in unweighted graphs",
        ],
        "code": {
            "python": "from collections import deque\n\n# Adjacency list representation\ngraph = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}\n\ndef bfs(graph, start):\n    visited = set([start])\n    queue = deque([start])\n    order = []\n    while queue:\n        node = queue.popleft()\n        order.append(node)\n        for neighbor in graph[node]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n    return order",
            "c": "// Adjacency matrix BFS\nvoid bfs(int graph[][MAX], int n, int start) {\n    int visited[MAX]={0}, queue[MAX], front=0, rear=0;\n    visited[start]=1; queue[rear++]=start;\n    while(front<rear){int v=queue[front++]; printf(\"%d \",v);\n        for(int i=0;i<n;i++) if(graph[v][i]&&!visited[i]){visited[i]=1;queue[rear++]=i;}}\n}",
            "cpp": "void bfs(vector<vector<int>>& adj, int start) {\n    vector<bool> visited(adj.size(), false);\n    queue<int> q;\n    visited[start] = true; q.push(start);\n    while (!q.empty()) {\n        int v = q.front(); q.pop(); cout << v << ' ';\n        for (int u : adj[v]) if (!visited[u]) { visited[u]=true; q.push(u); }\n    }\n}",
            "java": "void bfs(List<List<Integer>> adj, int start) {\n    boolean[] visited = new boolean[adj.size()];\n    Queue<Integer> q = new LinkedList<>();\n    visited[start] = true; q.offer(start);\n    while (!q.isEmpty()) {\n        int v = q.poll(); System.out.print(v + ' ');\n        for (int u : adj.get(v)) if (!visited[u]) { visited[u]=true; q.offer(u); }\n    }\n}",
        },
        "practice_problems": [
            {
                "title": "Find if a path exists between two nodes",
                "difficulty": "beginner",
                "hint1": "Use BFS or DFS starting from source node",
                "hint2": "If you reach the destination during traversal, path exists",
                "solution_approach": "BFS/DFS O(V+E): traverse from source, return True if destination is visited",
            },
        ],
    },
    "dynamic_programming": {
        "description": "Optimization technique that solves complex problems by breaking them into overlapping subproblems",
        "analogy": "Like remembering answers on a test — once you solve a subproblem, write it down so you never solve it twice",
        "time_complexity": {"varies": "Typically O(n) to O(n^2) depending on state space"},
        "space_complexity": "O(n) to O(n^2) for memoization table",
        "use_cases": ["Fibonacci sequence", "Longest common subsequence", "Knapsack problem", "Shortest path (Bellman-Ford)"],
        "steps": [
            "1. Identify if problem has OVERLAPPING SUBPROBLEMS and OPTIMAL SUBSTRUCTURE",
            "2. Define state: what information uniquely identifies a subproblem?",
            "3. Write the RECURRENCE RELATION: how does dp[i] depend on smaller states?",
            "4. Identify BASE CASES: the smallest subproblems you can answer directly",
            "5. Build table bottom-up (tabulation) or top-down with memoization",
        ],
        "code": {
            "python": "# Fibonacci with memoization (top-down DP)\ndef fib(n, memo={}):\n    if n in memo: return memo[n]\n    if n <= 1: return n\n    memo[n] = fib(n-1, memo) + fib(n-2, memo)\n    return memo[n]\n\n# Fibonacci with tabulation (bottom-up DP)\ndef fib_tab(n):\n    if n <= 1: return n\n    dp = [0] * (n + 1)\n    dp[1] = 1\n    for i in range(2, n + 1):\n        dp[i] = dp[i-1] + dp[i-2]\n    return dp[n]",
            "c": "int fib(int n) {\n    if (n <= 1) return n;\n    int dp[n+1]; dp[0]=0; dp[1]=1;\n    for(int i=2;i<=n;i++) dp[i]=dp[i-1]+dp[i-2];\n    return dp[n];\n}",
            "cpp": "int fib(int n) {\n    if (n <= 1) return n;\n    vector<int> dp(n+1); dp[0]=0; dp[1]=1;\n    for(int i=2;i<=n;i++) dp[i]=dp[i-1]+dp[i-2];\n    return dp[n];\n}",
            "java": "int fib(int n) {\n    if (n <= 1) return n;\n    int[] dp = new int[n+1]; dp[0]=0; dp[1]=1;\n    for(int i=2;i<=n;i++) dp[i]=dp[i-1]+dp[i-2];\n    return dp[n];\n}",
        },
        "practice_problems": [
            {
                "title": "Climbing stairs (1 or 2 steps at a time)",
                "difficulty": "beginner",
                "hint1": "How many ways to reach step n?",
                "hint2": "ways(n) = ways(n-1) + ways(n-2) — it's Fibonacci!",
                "solution_approach": "DP O(n): dp[i] = dp[i-1] + dp[i-2], base cases dp[1]=1, dp[2]=2",
            },
            {
                "title": "0/1 Knapsack problem",
                "difficulty": "advanced",
                "hint1": "For each item, you either include it or exclude it",
                "hint2": "dp[i][w] = max value using first i items with weight capacity w",
                "solution_approach": "2D DP O(n*W): dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]]) if wt[i]<=w",
            },
        ],
    },
}

_AVAILABLE_TOPICS = sorted(DSA_TOPICS.keys())


def _normalize_topic(topic: str) -> str | None:
    """Normalize topic string: lowercase, underscores/spaces interchangeable."""
    key = topic.strip().lower().replace(" ", "_").replace("-", "_")
    if key in DSA_TOPICS:
        return key
    # Fuzzy: try prefix match
    matches = [k for k in DSA_TOPICS if k.startswith(key) or key in k]
    return matches[0] if len(matches) == 1 else None


def _normalize_language(lang: str) -> str:
    """Normalize programming language name."""
    lang = lang.strip().lower()
    aliases = {
        "c++": "cpp",
        "c plus plus": "cpp",
        "cplusplus": "cpp",
        "c#": "c",  # map to c (no C# in data)
    }
    return aliases.get(lang, lang)


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------


@tool
def explain_concept(topic: str, skill_level: str = "beginner", language: str = "english") -> str:
    """Explain a DSA concept with a real-world analogy, step-by-step logic, and complexity analysis.

    Args:
        topic: The DSA topic to explain (e.g. 'array', 'binary_search', 'recursion').
        skill_level: 'beginner', 'intermediate', or 'advanced'.
        language: 'english' or 'tamil'.
    """
    key = _normalize_topic(topic)
    if key is None:
        available = ", ".join(_AVAILABLE_TOPICS)
        return (
            f"I don't have structured content for '{topic}' yet.\n"
            f"Available topics: {available}\n"
            "Please ask about one of these, or ask me to explain the concept in my own words!"
        )

    data = DSA_TOPICS[key]
    lines = []

    if language.lower() == "tamil":
        lines.append("Kurrippu: Inda vilaakkam tamilil vangappadukiradu (Tamil explanation below)\n")
        lines.append(f"**{key.replace('_', ' ').title()}** (tharavu kattamaippu / Data Structure)\n")
    else:
        lines.append(f"## {key.replace('_', ' ').title()}\n")

    lines.append(f"**What it is:** {data['description']}")
    lines.append(f"**Real-world analogy:** {data['analogy']}")

    if skill_level in ("intermediate", "advanced"):
        lines.append(f"\n**Time Complexity:** {data['time_complexity']}")
        lines.append(f"**Space Complexity:** {data['space_complexity']}")

    lines.append("\n**Step-by-step logic:**")
    for step in data["steps"]:
        lines.append(f"  {step}")

    lines.append(f"\n**Common use cases:** {', '.join(data['use_cases'])}")

    if skill_level == "advanced":
        lines.append(f"\n**Full complexity breakdown:** {data['time_complexity']}")
        lines.append(f"**Space:** {data['space_complexity']}")

    if language.lower() == "tamil":
        lines.append("\n**Mukkiya vaarththaigal (Key terms):**")
        lines.append("  - Data Structure = Tharavu Kattamaippu")
        lines.append("  - Algorithm = Vazhimurai")
        lines.append("  - Time Complexity = Nera Sikkalanathu")
        lines.append("  - Space Complexity = Ida Sikkalanathu")

    return "\n".join(lines)


@tool
def show_code(algorithm: str, programming_language: str = "python", explanation_level: str = "detailed") -> str:
    """Show code for a DSA algorithm in a specific programming language with explanation.

    Args:
        algorithm: The algorithm or data structure (e.g. 'binary_search', 'bubble_sort').
        programming_language: 'python', 'c', 'cpp', or 'java'.
        explanation_level: 'basic' for code only, 'detailed' for line-by-line comments.
    """
    key = _normalize_topic(algorithm)
    if key is None:
        available = ", ".join(_AVAILABLE_TOPICS)
        return f"No code found for '{algorithm}'. Available topics: {available}"

    lang = _normalize_language(programming_language)
    data = DSA_TOPICS[key]
    code_map: dict[str, str] = data.get("code", {})

    if lang not in code_map:
        supported = ", ".join(code_map.keys())
        return f"No {programming_language} code for '{key}'. Supported languages: {supported}"

    code = code_map[lang]
    lines = [f"## {key.replace('_', ' ').title()} — {lang.upper() if lang != 'python' else 'Python'}\n"]
    lines.append(f"```{lang if lang != 'cpp' else 'cpp'}")
    lines.append(code)
    lines.append("```\n")

    if explanation_level == "detailed":
        lines.append("**Algorithm steps this code implements:**")
        for step in data["steps"]:
            lines.append(f"  {step}")
        tc = data["time_complexity"]
        lines.append(f"\n**Time complexity:** {tc}")
        lines.append(f"**Space complexity:** {data['space_complexity']}")

    lines.append("\n**Try it with:** a small example input and trace through each line.")
    return "\n".join(lines)


@tool
def get_practice_problems(topic: str, difficulty: str = "beginner", preferred_language: str = "python") -> str:
    """Get practice problems for a DSA topic with progressive hints.

    Args:
        topic: The DSA topic (e.g. 'array', 'linked_list', 'binary_search').
        difficulty: 'beginner', 'intermediate', or 'advanced'.
        preferred_language: Preferred programming language for code examples.
    """
    key = _normalize_topic(topic)
    if key is None:
        available = ", ".join(_AVAILABLE_TOPICS)
        return f"No practice problems for '{topic}'. Available topics: {available}"

    data = DSA_TOPICS[key]
    problems: list[dict] = data.get("practice_problems", [])

    if not problems:
        return f"No practice problems stored for '{key}' yet. Try asking me to generate one!"

    # Filter by difficulty if possible; fall back to all
    filtered = [p for p in problems if p.get("difficulty") == difficulty]
    if not filtered:
        filtered = problems

    lang = _normalize_language(preferred_language)
    lines = [f"## Practice Problems: {key.replace('_', ' ').title()} ({difficulty})\n"]

    for i, prob in enumerate(filtered, 1):
        lines.append(f"### Problem {i}: {prob['title']}")
        lines.append(f"**Difficulty:** {prob.get('difficulty', difficulty)}\n")
        lines.append(f"**Hint 1:** {prob['hint1']}")
        lines.append(f"**Hint 2 (read only if stuck):** {prob['hint2']}")
        lines.append(f"\n**Solution approach (read only after attempting):**")
        lines.append(f"  {prob['solution_approach']}")
        lines.append("")

    lines.append(f"*Try solving in {lang}. Ask me to review your solution when you're done!*")
    return "\n".join(lines)


@tool
def compare_implementations(algorithm: str, programming_languages: str = "python,java") -> str:
    """Compare the implementation of an algorithm across multiple programming languages.

    Args:
        algorithm: The algorithm or data structure to compare (e.g. 'binary_search').
        programming_languages: Comma-separated list of languages (e.g. 'python,java,cpp').
    """
    key = _normalize_topic(algorithm)
    if key is None:
        available = ", ".join(_AVAILABLE_TOPICS)
        return f"No code found for '{algorithm}'. Available topics: {available}"

    data = DSA_TOPICS[key]
    code_map: dict[str, str] = data.get("code", {})

    langs = [_normalize_language(l.strip()) for l in programming_languages.split(",") if l.strip()]
    if not langs:
        langs = ["python", "java"]

    lines = [f"## {key.replace('_', ' ').title()} — Language Comparison\n"]
    lines.append(f"**Core idea:** {data['description']}")
    lines.append(f"**The logic is the same in all languages — only syntax differs.**\n")

    shown = 0
    for lang in langs:
        if lang in code_map:
            display = lang.upper() if lang in ("c", "cpp", "java") else lang.capitalize()
            lines.append(f"### {display}")
            lines.append(f"```{lang}")
            lines.append(code_map[lang])
            lines.append("```\n")
            shown += 1
        else:
            available_langs = ", ".join(code_map.keys())
            lines.append(f"*No {lang} example available. Supported: {available_langs}*\n")

    if shown > 1:
        lines.append("## Key Differences\n")
        if "python" in langs and "java" in langs:
            lines.append("- **Python:** no type declarations, concise syntax, list/deque built-ins")
            lines.append("- **Java:** explicit types, verbose but clear, standard library classes")
        if "c" in langs:
            lines.append("- **C:** manual memory management, raw arrays, pointer arithmetic")
        if "cpp" in langs:
            lines.append("- **C++:** STL containers (vector, stack, queue) simplify the code vs C")
        lines.append("\n**The underlying algorithm and time complexity are identical across all languages.**")

    return "\n".join(lines)


@tool
def debug_code(code: str, programming_language: str = "python") -> str:
    """Analyze student code for common DSA mistakes and guide them toward the fix.

    Does NOT give the corrected code directly — guides the student to find the fix themselves.

    Args:
        code: The student's code to analyze.
        programming_language: The programming language of the code.
    """
    lang = _normalize_language(programming_language)
    issues_found: list[str] = []
    hints: list[str] = []

    code_lower = code.lower()

    # Off-by-one in binary search
    if "binary" in code_lower or ("left" in code_lower and "right" in code_lower and "mid" in code_lower):
        if "len(arr)" in code and "right" in code and "<" in code and "<=" not in code.split("right")[0]:
            issues_found.append("Possible off-by-one: `right = len(arr)` (should be `len(arr) - 1` for 0-based indexing)")
            hints.append("Think about what index `len(arr)` points to — is it a valid array position?")
        if "left = mid" in code and "left = mid + 1" not in code:
            issues_found.append("Infinite loop risk: `left = mid` instead of `left = mid + 1`")
            hints.append("If arr[mid] < target and you set left = mid (not mid+1), what happens when left==mid?")
        if "right = mid" in code and "right = mid - 1" not in code:
            issues_found.append("Infinite loop risk: `right = mid` instead of `right = mid - 1`")
            hints.append("If arr[mid] > target and right = mid, can left ever exceed right?")

    # Bubble sort loop bound
    if "bubble" in code_lower or ("swap" in code_lower and "for" in code_lower):
        if "range(n)" in code and "range(n - i - 1)" not in code and "range(n-i-1)" not in code:
            issues_found.append("Inner loop may not shrink: missing `n - i - 1` bound optimization")
            hints.append("After pass i, the last i elements are already sorted. Does your inner loop still touch them?")

    # Missing base case in recursion
    if "def " in code and ("return " + code.split("def ")[1].split("(")[0].strip() if "def " in code else "") in code:
        if "if" not in code_lower[:code_lower.find("return")]:
            issues_found.append("Possible missing base case in recursive function")
            hints.append("Every recursive function needs a base case to stop recursion. What is yours?")

    # Null/None pointer in linked list
    if "node" in code_lower and ("next" in code_lower):
        if ".next.next" in code and "if" not in code_lower:
            issues_found.append("Possible NullPointerException: accessing .next.next without None check")
            hints.append("Before accessing node.next.next, check that node.next is not None first.")

    # Stack underflow
    if ("pop()" in code or "pop(" in code) and "if" not in code_lower[:code_lower.find("pop")]:
        issues_found.append("Possible stack/list underflow: calling pop() without checking if collection is empty")
        hints.append("What happens if you call pop() on an empty list/stack? Add an isEmpty check first.")

    lang_label = lang.upper() if lang in ("c", "cpp", "java") else lang.capitalize()
    lines = [f"## Code Review ({lang_label})\n"]
    lines.append("I'll guide you toward finding the bug — learning is better than just getting the answer!\n")

    if issues_found:
        lines.append("### Potential Issues Found\n")
        for i, issue in enumerate(issues_found, 1):
            lines.append(f"**Issue {i}:** {issue}")
        lines.append("\n### Guided Hints\n")
        for i, hint in enumerate(hints, 1):
            lines.append(f"**Hint {i}:** {hint}")
        lines.append("\n### Next Steps")
        lines.append("1. Read each hint carefully and trace through your code manually with a small example.")
        lines.append("2. Write down the values of your variables at each step.")
        lines.append("3. Ask me to check your fix once you've made a change!")
    else:
        lines.append("### No obvious common mistakes detected.\n")
        lines.append("The code looks structurally reasonable. To go deeper:")
        lines.append("1. **Trace it manually:** run your code on paper with a small example (3-5 elements).")
        lines.append("2. **Check edge cases:** empty input, single element, all same elements, sorted/reverse-sorted.")
        lines.append("3. **Tell me what output you expect vs what you get** — that helps me pinpoint the issue.")

    lines.append("\n*Remember: understanding why it's wrong matters more than the fix!*")
    return "\n".join(lines)


TOOLS = [explain_concept, show_code, get_practice_problems, compare_implementations, debug_code]
