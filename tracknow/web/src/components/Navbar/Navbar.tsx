import * as React from "react";
import {
    Box,
    Flex,
    Text,
    Stack,
    Button,
    Center,
    useColorModeValue,
    Link,
    Avatar,
    Menu,
    MenuButton,
    MenuDivider,
    MenuItem,
    MenuList
} from "@chakra-ui/react";
import { AddIcon } from '@chakra-ui/icons'
import { Link as ReactRouterLink } from 'react-router-dom';
import { identityProfile } from "../../Types";
import useMiscFunctions from "../../misc/miscFunctions";


// TODO move link styles to tracknowTheme

export const NavbarWelcome = () => (
    <Box px={4} borderBottom={1} borderStyle={'solid'} borderColor={useColorModeValue('dark', 'white')}>
        <Flex h={10} alignItems={'center'} justifyContent={'space-between'}>

            <Box><Link as={ReactRouterLink} to="/home" _hover={{ textDecoration: 'none' }} style={{ textDecoration: 'none', color: 'inherit' }}><Text fontSize="xl" as="b">tracknow</Text></Link></Box>
            <Flex alignItems={'center'}>
                <Stack direction={'row'} spacing={7}>
                    <Link _hover={{ textDecoration: 'none' }} style={{ textDecoration: 'none', fontWeight: "bold", color: 'inherit' }} as={ReactRouterLink} to={'/login'} >login</Link>
                    {/*
                    <Center>
                        <Text as='del' >Leaderboard</Text> coming soon
                    </Center>
                    */}
                </Stack>
            </Flex>

        </Flex>
    </Box>
);

export const Navbar = () => (
    <Box px={4} borderBottom={1} borderStyle={'solid'} borderColor={useColorModeValue('dark', 'white')}>
        <Flex h={10} alignItems={'center'} justifyContent={'space-between'}>

            <Box>
                <Link as={ReactRouterLink} to="/home" _hover={{ textDecoration: 'none' }} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <Text fontSize="xl" as="b">
                        tracknow
                    </Text>
                </Link></Box>

            <Flex alignItems={'center'}>
                <Stack direction={'row'} spacing={7}>
                    {/* 
                    <Center>
                        <Text as='del' >Leaderboard</Text>
                    </Center>
                    */}
                </Stack>
            </Flex>
        </Flex>
    </Box>
);


export const NavbarLoggedIn = ({ name, pp }: identityProfile) => {
    const { handleLogout } = useMiscFunctions();
    return (
        <Box
            position="fixed"
            top="0"
            left="0"
            right="0"
            zIndex={1}
            bg={"dark"}
            px={4}
            borderBottom={1}
            borderStyle={"solid"}
            borderColor={useColorModeValue("#323536", "white")}
        >
            <Flex h={10} alignItems={"center"} justifyContent={'space-between'}>
                <Box>
                    <Link as={ReactRouterLink} to="/home" _hover={{ textDecoration: 'none' }} style={{ textDecoration: 'none', color: 'inherit' }}>
                        <Text fontSize="xl" as="b">
                            tracknow
                        </Text>
                    </Link>
                </Box>

                <Flex alignItems={"center"}>
                    <Stack direction={"row"} spacing={1}>
                        <Button
                            size={"sm"}
                            variant="navbarButton"
                            as={ReactRouterLink}
                            to={`/user/${name}/create-moments`}
                            leftIcon={<AddIcon />}>
                            Create
                        </Button>
                        <Menu>
                            <MenuButton
                                as={Button}
                                rounded={'full'}
                                variant={'link'}
                                cursor={'pointer'}
                                minW={0}>
                                <Avatar
                                    size={'sm'}
                                    src={pp}
                                />

                            </MenuButton>
                            <MenuList alignItems={'center'} >
                                <br />
                                <Center>
                                    <Avatar
                                        size={'2xl'}
                                        src={pp}
                                    />
                                </Center>
                                <br />
                                <Center>
                                    <p>{name}</p>
                                </Center>
                                <br />
                                <MenuDivider />
                                <MenuItem as={ReactRouterLink} to={`/user/${name}/my-moments`}>My Moments</MenuItem>
                                <MenuItem as={ReactRouterLink} to={`/user/${name}/account-settings`}>Account Settings</MenuItem>
                                <MenuItem onClick={handleLogout}>Logout</MenuItem>
                            </MenuList>
                        </Menu>
                    </Stack>
                </Flex>
            </Flex>

        </Box>
    );
};