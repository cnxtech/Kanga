import builder


def main():
    stdout = ''
    try:
        topology_name = 'KangaTopology26'
        topology_src_file = topology_name+'.java'
        paths = builder.get_paths()
        builder.clean(paths,10)
        stdout = builder.run_ant(topology_name, topology_src_file, paths)+'\n\n'
        stdout += builder.submit_topology(topology_name, topology_src_file, paths)
    except Exception as e:
        print 'error --> '+str(e)
    print stdout

if __name__ == "__main__":
    main()