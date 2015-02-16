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

--g) 
--select 
--       case  
--       	    when e.job is null  then 'toutemploye' 
--       	    when e.job is not null then e.job 
--       end as 'fkk'  
--from emp e 
--     group by rollup(e.deptno,e.job);
--,sum(e.sal) e.deptno,

--exo 2

--1)
select
	t.annee,
	c.cl_r,
	p.category,
	avg(v.pu*v.qte) ca_moyen
from ventes v, clients c, produits p, temps t
where v.tid = t.tid and v.cid = c.cl_id and v.pid = p.pid and (t.annee = 2009 or t.annee = 2010)
group by rollup(t.annee, c.cl_r, p.category);

--2)
select
	t.annee,
	c.cl_r,
	p.category,
	avg(v.pu * v.qte) ca_moyen
from ventes v, clients c, produits p, temps t
where v.tid = t.tid and v.cid = c.cl_id and v.pid = p.pid and (t.annee = 2009 or t.annee = 2010)
group by cube(t.annee, c.cl_r, p.category);

--3) no good
--select
--	distinct rank() over (partition by t.annee, p.category order by v.qte) rank,
--	t.annee,
--	p.category,
--	p.pname
--from ventes v, produits p, temps t
--where v.tid = t.tid and v.pid = p.pid;


select
	distinct rank() over(partition by p.category order by -v.qte) rank,
	p.category,
	p.pname,
	v.qte
from ventes v, produits p, temps t
where v.tid = t.tid and v.pid = p.pid and p.category = 'Viandes';

--4)
select annee,category, CA
from (select t.annee, p.category, sum(v.pu*v.qte) CA, grouping_id(t.annee) gc
  from produits p, ventes v, temps t
  where (v.pid=p.pid and v.tid=t.tid)
  group by rollup (t.annee,p.category))
where gc = 0;

--5)
select annee, mois, CA_TOTAL
from (select annee, mois, CA_TOTAL, rank() over (partition by annee order by -CA_TOTAL) rank
      from (select t.annee, t.mois, sum(v.pu * v.qte) CA_TOTAL
            from temps t, ventes v, produits p
            where (v.pid=p.pid and v.tid=t.tid) and p.pname='Sirop d ¿¿rable'
            group by(t.annee, t.mois)))
where rank = 1;

--6)
select t.annee, c.cl_name, p.category, sum(v.pu * v.qte) CA_TOTAL
from temps t, ventes v, produits p, clients c
where (v.pid = p.pid and v.tid = t.tid and v.cid = c.cl_id)
group by grouping sets((t.annee, c.cl_name), (t.annee, p.category));

--7)
select category, QTE_VENDUE_2010, ntile(3) over (order by QTE_VENDUE_2010 desc) tiers
from (select p.category, sum(v.qte) QTE_VENDUE_2010
      from ventes v, produits p, temps t
      where (v.pid = p.pid and v.tid = t.tid) and t.annee = 2010
      group by(p.category));
      
--8)
select p.category, t.mois, sum(v.qte)
from ventes v, temps t, produits p
where (v.tid = t.tid and v.pid = p.pid) and t.annee = 2010 and t.jour >= 1 and t.jour <= 5
group by(p.category, t.mois)
order by t.mois, p.category;