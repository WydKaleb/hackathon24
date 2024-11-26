const groups = [
    { id: 1, name: 'BHANK', members: ['Bhavya', 'Harleen', 'Andrew', 'Nimi', 'Kaleb'] },
    { id: 2, name: 'Group 2', members: ['Charlie', 'Dana'] },
];

const groupContainer = document.getElementById('mentor-groups');

// Function to display all groups/members
function displayGroups() {
    groupContainer.innerHTML = ''; // Clearing container before rendering groups

    // Loop over each group in the array
    groups.forEach(group => {
        // Creating a box for each group
        const groupBox = document.createElement('div');
        groupBox.classList.add('group-box');
        
        // Create a container for group info (name and members)
        const groupInfo = document.createElement('div');
        groupInfo.classList.add('group-info');

        // Defining group name
        const groupName = document.createElement('h3');
        groupName.innerText = group.name;
        groupInfo.appendChild(groupName);

        // List of members
        const memberList = document.createElement('ul');
        group.members.forEach(member => {
            const memberToAdd = document.createElement('li');
            memberToAdd.innerText = member;
            memberList.appendChild(memberToAdd);
        });
        groupInfo.appendChild(memberList);

        // Creating container for the add/remove buttons
        const actionButtons = document.createElement('div');
        actionButtons.classList.add('group-actions');

        // Button to add a member
        const addButton = document.createElement('button');
        addButton.classList.add('add-button');
        addButton.innerText = 'Add Member';
        addButton.addEventListener('click', () => addMember(group.id));
        actionButtons.appendChild(addButton);

        // Button to remove a member
        const removeButton = document.createElement('button');
        removeButton.classList.add('remove-button');
        removeButton.innerText = 'Remove Member';
        removeButton.addEventListener('click', () => removeMember(group.id));
        actionButtons.appendChild(removeButton);

        // Appending everything to the group box
        groupBox.appendChild(groupInfo);
        groupBox.appendChild(actionButtons);

        // Appending the group box to the group container
        groupContainer.appendChild(groupBox);
    });

    // After loop finishes, adding "Create New Group" button at the bottom
    addCreateGroupButton();
}

// Function to add a member to a group
function addMember(groupId) {
    const memberName = prompt('Enter the name of the member to add:');
    if (memberName) {
        const group = groups.find(group => group.id === groupId);
        if (group) {
            group.members.push(memberName); // Adding member to the group
            displayGroups(); // Re-render groups with updated members
        }
    }
}

// Function to remove a member from a group
function removeMember(groupId) {
    const memberName = prompt('Enter the name of the member to remove:');
    if (memberName) {
        const group = groups.find(group => group.id === groupId);
        if (group) {
            group.members = group.members.filter(member => member !== memberName); // Removing member
            displayGroups(); // Re-render groups with updated members
        }
    }
}

// Function to add a new group
function createNewGroup() {
    const groupName = prompt('Enter the name of the new group:');
    const memberNames = prompt('Enter the members of the group, separated by commas:');
    if (groupName && memberNames) {
        const newGroup = {
            id: groups.length + 1,
            name: groupName,
            members: memberNames.split(',').map(name => name.trim()) // Removing commas and spaces
        };
        groups.push(newGroup); // Add the new group to the groups array
        displayGroups(); // Re-render groups with the new group
    }
}

// Function to add the "Create New Group" button at the bottom
function addCreateGroupButton() {
    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('new-group-container');
    
    const createGroupButton = document.createElement('button');
    createGroupButton.classList.add('create-group-button');
    createGroupButton.innerText = 'Create New Group';
    createGroupButton.addEventListener('click', createNewGroup);

    buttonContainer.appendChild(createGroupButton);

    // Append the button container to the main group container
    groupContainer.appendChild(buttonContainer);
}

// Call displayGroups initially to load groups
window.onload = displayGroups;