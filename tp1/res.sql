
--exo 1) a)
select distinct e.deptno,e.ename,e.sal,
	rank()over(partition by e.deptno order by -e.sal) rank 
	from emp e 
	where e.deptno=10 or e.deptno=30 
	order by e.deptno,-e.sal;

-- b) on enleve les trou en rajoutant dense_rank() a la place de rank()
select distinct e.deptno,e.ename,e.sal,
	dense_rank()over(partition by e.deptno order by -e.sal) rank 
	from emp e 
	where e.deptno=10 or e.deptno=30 
	order by e.deptno,-e.sal;

--c)
select distinct e.deptno,e.sal,
	dense_rank()over(partition by e.deptno order by -e.sal) rank 
	from emp e where e.deptno=10 or e.deptno=20 
	order by e.deptno,-e.sal;
--d) ac group by
select e.job,sum(e.sal) from emp e group by job;
    --ac partition by
select distinct  e.job,sum(e.sal) over(partition by job) from emp e  ;


--e) La difference entre Group By et Partition By : TODO

--f)
select e.deptno,e.job,sum(e.sal) 
	from emp e 
	group by rollup(e.deptno,e.job);

--g) TODO
select e.deptno, case grouping(e.job) when 1 then 'toutemploye' else e.job end as 'knjn',sum(e.sal) from emp e group by rollup(e.deptno,e.job);

