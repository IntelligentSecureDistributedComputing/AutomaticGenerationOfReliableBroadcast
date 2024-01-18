
/*****************************************************/
                        /*INPUT*/
/*****************************************************/

/*N*/

/*F*/

/*N_Types*/

/*VALIDITY*/

/*INTEGRITY*/

/*AGREEMENT*/

/*PROCESS_BROADCASTING*/

/*****************************************************/
                /*GLOBAL VARIABLES*/
/*****************************************************/

/**/
#define N_Messages 3
#define VALID_MESSAGE 1
#define BYZANTINE_MESSAGE 2
/**/
#define NO_FAILURE 0
#define CRASH_FAILURE 1
#define BYZANTINE_FAILURE 2
/**/
#define TYPE 0
/**/
typedef content {
    int m[N_Messages]
}
/**/
typedef types {
    content t[N_Types]
}
/**/
typedef sender {
    types s[N]
}
/**/
typedef neighbours {
    int n[N]
}
/**/
int failure_mode_state[N] = NO_FAILURE;
/**/
content messages_delivered[N];
/**/
neighbours process_neighbours[N];
/**/
sender pr[N];
/**/
chan inputChannel[N] = [50] of {int,int,int}

/*****************************************************/
                    /*PROCESS*/
/*****************************************************/

proctype Proc(int ID) {

types mr;
int type,msg,from,i,neighbour,t,status;
chan channel = inputChannel[ID];
xr channel;

/*****************************************************/
                /*DECISION PATH*/
/*****************************************************/
    
atomic
{
if
:: PROCESS_BROADCASTING == ID ->
    goto broadcast_step;
:: else ->
    goto communication_step;
fi;
}
    
/*****************************************************/
                  /*BROADCAST EVENT*/
/*****************************************************/



broadcast_step:

atomic{

msg = VALID_MESSAGE; 
if
:: failure_mode_state[ID]==NO_FAILURE || failure_mode_state[ID]==CRASH_FAILURE  -> /** if is a correct process or a crash process */

/*BROADCAST_STEP*/

:: failure_mode_state[ID]==BYZANTINE_FAILURE-> /** if is a byzantine process */

/*BROADCAST_ATTACKS*/

fi;

goto communication_step;

}

/*****************************************************/
                /*COMMUNICATION EVENT*/
/*****************************************************/

communication_step:

atomic{

if
:: failure_mode_state[ID]==NO_FAILURE || failure_mode_state[ID]==CRASH_FAILURE-> /** if is a correct process or a crash process */
if
::channel?type,msg,from -> /*receive message*/
mr.t[type].m[msg]++; /*store message*/

/*COMMUNICATION_STEP*/

goto communication_step;

::timeout -> /*execution ends*/

goto end_step;

fi;

:: failure_mode_state[ID]==BYZANTINE_FAILURE-> /** if is a byzantine process */

/*COMMUNICATION_ATTACKS*/

goto end_step;

fi;


}
/*****************************************************/
                    /*END STATE*/
/*****************************************************/

end_step: /**  process stops */
}


/*****************************************************/
                     /*INIT*/
/*****************************************************/

init
{

/*****************************************************/
                /*FAILURE DECISION*/
/*****************************************************/

/*FAULTY_DECISION*/

/*****************************************************/
                  /*RUN PROCESSES*/
/*****************************************************/

atomic
{

/*SYSTEM_ARCHITECTURE*/

}

/*****************************************************/
                   /* VALIDATION */
/*****************************************************/

(_nr_pr == 1);
int a,b,c;

/*****************************************************/
                   /* VALIDATION */
/*****************************************************/

if
:: VALIDITY ->
    if
    :: failure_mode_state[PROCESS_BROADCASTING]==NO_FAILURE ->
        if 
        :: failure_mode_state[PROCESS_BROADCASTING]==NO_FAILURE && messages_delivered[PROCESS_BROADCASTING].m[VALID_MESSAGE] == 0 ->
            assert(false);
        ::else;
        fi;
    ::else;
    fi;
:: else;
fi;
    
/*****************************************************/
                    /* INTEGRITY */
/*****************************************************/

if
:: INTEGRITY ->
    a=0;
    do
    :: a<N ->
        if
        :: failure_mode_state[a]==NO_FAILURE ->
            c=0;
            do
            :: c<N_Messages ->
                if 
                :: messages_delivered[a].m[c]>1 || (failure_mode_state[PROCESS_BROADCASTING] == NO_FAILURE && messages_delivered[a].m[c] > 0 && c!=VALID_MESSAGE) ->
                    assert(false)
                :: else;
                fi;
                c++;
            ::break;
            od;
        :: else;
        fi;
        a++;
    ::break;
    od;
:: else;
fi;

/*****************************************************/
                    /* AGREEMENT */
/*****************************************************/

if
:: AGREEMENT ->
        a=0;
        do
        :: a<N ->
            if
            :: failure_mode_state[a]==NO_FAILURE ->
                b=0
                do
                :: b<N ->
                    if
                    :: failure_mode_state[b]==NO_FAILURE ->
                        c=0
                        do
                        :: c<N_Messages ->
                            if 
                            :: messages_delivered[a].m[c] > 0 ->
                                if
                                :: messages_delivered[b].m[c]==0 ->
                                    assert(false)
                                :: else;
                                fi
                            :: else;
                            fi;
                            c++;
                        ::break;
                        od;
                    :: else;
                    fi;
                    b++;
                :: break;
                od;
            :: else;
            fi;
            a++;
        ::break;
        od;
:: else;
fi;
}

